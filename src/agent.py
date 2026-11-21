"""LangGraph agent: plan -> retrieve -> answer -> groundedness check.

The graph runs fully offline. The answer node composes its answer ONLY
from retrieved passages using a deterministic extractive composer. If an
OpenAI-compatible API key is present in the environment
(OPENAI_API_KEY), an optional provider path is used for composition --
but the groundedness node still verifies every sentence against the
retrieved passages before anything is returned.

Configuration (environment variables, see .env.example):
  RAG_DOCS_DIR           corpus directory (default: ../corpus)
  RAG_GROUNDING_THRESHOLD  sentence-overlap threshold for the
                         groundedness check (default: 0.35)
  OPENAI_API_KEY / OPENAI_MODEL / OPENAI_BASE_URL
                         optional provider composition path
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from retrieval import Hit, HybridIndex, tokenise

DOCS_DIR = Path(
    os.environ.get(
        "RAG_DOCS_DIR",
        Path(__file__).resolve().parent.parent / "corpus",
    )
)
MAX_ATTEMPTS = 2
DEFAULT_GROUNDING_THRESHOLD = 0.35


def _default_threshold() -> float:
    try:
        return float(os.environ.get("RAG_GROUNDING_THRESHOLD",
                                    DEFAULT_GROUNDING_THRESHOLD))
    except ValueError:
        return DEFAULT_GROUNDING_THRESHOLD


class AgentState(TypedDict, total=False):
    question: str
    plan: str
    query: str
    hits: list[Hit]
    answer: str
    claims: list[dict]
    grounded: bool
    attempts: int
    abstained: bool
    threshold: float


# ---------------------------------------------------------------- nodes

def plan_node(state: AgentState) -> AgentState:
    """Route/plan: classify the question and form the retrieval query."""
    q = state["question"]
    lowered = q.lower()
    if any(w in lowered for w in ("example", "code", "show me")):
        plan = "code-example lookup"
    elif any(w in lowered for w in ("difference", "compare", "vs")):
        plan = "comparison lookup"
    elif lowered.startswith(("what is", "what are", "what does")):
        plan = "concept lookup"
    elif any(w in lowered for w in ("how", "steps", "build")):
        plan = "how-to lookup"
    else:
        plan = "concept lookup"
    return {"plan": plan, "query": q, "attempts": state.get("attempts", 0)}


def make_retrieve_node(index: HybridIndex):
    def retrieve_node(state: AgentState) -> AgentState:
        query = state["query"]
        # Retry widens the net (larger top-k) on the SAME query --
        # adding new words would retrieve passages about those words,
        # not about the question.
        top_k = 8 if state.get("attempts", 0) > 0 else 4
        return {"hits": index.search(query, top_k=top_k), "query": query}

    return retrieve_node


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 25]


def _compose_offline(question: str, hits: list[Hit]) -> str:
    """Deterministic extractive composer: rank sentences inside the
    retrieved passages by overlap with the question, keep the best."""
    qtokens = set(tokenise(question))
    scored: list[tuple[float, str]] = []
    seen: set[str] = set()
    for hit in hits:
        for sent in _sentences(hit.chunk.text):
            if sent.startswith(("#", "Source:", "License:")):
                continue
            if not sent[0].isupper():
                continue  # fragment left by chunk overlap, not a sentence
            key = sent.lower()
            if key in seen:
                continue
            seen.add(key)
            overlap = len(qtokens & set(tokenise(sent)))
            if overlap:
                scored.append((overlap + hit.score, sent))
    scored.sort(key=lambda x: x[0], reverse=True)
    picked = [s for _, s in scored[:4]]
    return " ".join(picked)


def _compose_with_provider(question: str, hits: list[Hit]) -> str | None:
    """Optional OpenAI-compatible composition. Returns None on any
    failure so the offline composer remains the fallback."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        import json
        import urllib.request

        context = "\n\n".join(h.chunk.text for h in hits)
        payload = {
            "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            "messages": [
                {"role": "system",
                 "content": "Answer using ONLY the provided passages. "
                            "Do not add facts that are not in them."},
                {"role": "user",
                 "content": f"Passages:\n{context}\n\nQuestion: {question}"},
            ],
        }
        req = urllib.request.Request(
            os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
            + "/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


def answer_node(state: AgentState) -> AgentState:
    hits = state.get("hits", [])
    if not hits:
        return {"answer": "", "attempts": state.get("attempts", 0) + 1}
    answer = _compose_with_provider(state["question"], hits)
    if answer is None:
        answer = _compose_offline(state["question"], hits)
    return {"answer": answer, "attempts": state.get("attempts", 0) + 1}


def groundedness_node(state: AgentState) -> AgentState:
    """Self-check: every answer sentence must trace to a retrieved
    passage. A sentence is grounded when at least `threshold` of its
    content tokens appear in some single retrieved passage."""
    threshold = state.get("threshold", _default_threshold())
    hits = state.get("hits", [])
    answer = state.get("answer", "")
    passage_tokens = [set(tokenise(h.chunk.text)) for h in hits]
    claims: list[dict] = []
    all_grounded = bool(answer) and bool(hits)
    for sent in _sentences(answer):
        stoks = set(tokenise(sent))
        best = 0.0
        best_src = None
        for hit, ptoks in zip(hits, passage_tokens):
            if stoks:
                ratio = len(stoks & ptoks) / len(stoks)
                if ratio > best:
                    best, best_src = ratio, hit.chunk.source
        grounded = best >= threshold
        all_grounded = all_grounded and grounded
        claims.append({"sentence": sent, "grounded": grounded,
                       "overlap": round(best, 2), "source": best_src})
    abstained = not all_grounded and state.get("attempts", 0) >= MAX_ATTEMPTS
    return {"claims": claims, "grounded": all_grounded, "abstained": abstained}


def route_after_check(state: AgentState) -> str:
    if state.get("grounded"):
        return END
    if state.get("attempts", 0) >= MAX_ATTEMPTS:
        return END  # abstain: answer is replaced by the caller
    return "retrieve"


# ---------------------------------------------------------------- graph

def build_graph(index: HybridIndex):
    graph = StateGraph(AgentState)
    graph.add_node("plan", plan_node)
    graph.add_node("retrieve", make_retrieve_node(index))
    graph.add_node("answer", answer_node)
    graph.add_node("groundedness_check", groundedness_node)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", "groundedness_check")
    graph.add_conditional_edges("groundedness_check", route_after_check,
                                {"retrieve": "retrieve", END: END})
    return graph.compile()


def run_agent(question: str, docs_dir: Path = DOCS_DIR,
              threshold: float | None = None) -> AgentState:
    index = HybridIndex(docs_dir)
    app = build_graph(index)
    result = app.invoke({
        "question": question,
        "attempts": 0,
        "threshold": _default_threshold() if threshold is None else threshold,
    })
    if result.get("abstained") or not result.get("grounded"):
        result["answer"] = (
            "I could not ground an answer to that question in the "
            "document set, so I am abstaining rather than guessing."
        )
    return result
