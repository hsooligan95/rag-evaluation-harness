# RAG Evaluation Harness

A retrieval-augmented generation (RAG) system that **verifies its own
answers before returning them** — plus the labeled evaluation harness
that measures whether it actually works: retrieval quality, answer
groundedness, and abstention behavior, with per-case diagnosis and
threshold tuning.

Most RAG demos stop at "it answered." This project is about the harder
question: *should it have answered, and can every sentence be traced
back to a retrieved passage?* When the answer can't be grounded in the
corpus, the system abstains instead of guessing.

It runs **end to end offline** — no API key, no paid services. The
retrieval layer is standard-library only (BM25 + TF-IDF hybrid), and
answers are composed extractively from retrieved passages. An optional
OpenAI-compatible provider path exists, and its output has to pass the
same groundedness check.

## The system under evaluation

A LangGraph state machine over a bundled corpus of 16 public
documentation notes (LangGraph, LangChain, and Python — see
`corpus/ATTRIBUTION.md`):

1. **Plan / route** — classifies the question and forms the query.
2. **Retrieve** — paragraph-chunks the corpus and runs hybrid search
   (BM25 keyword scores blended 50/50 with TF-IDF cosine similarity),
   returning the top passages **with their sources**, behind a
   relevance gate (a passage must share ≥2 distinct query tokens).
3. **Answer** — composes an answer **only from the retrieved
   passages**, so every claim carries a citation trail.
4. **Groundedness check** — every answer sentence is scored against
   the retrieved passages (fraction of its content tokens appearing in
   a single passage). Below the threshold, the graph retries once with
   a wider retrieval pass; still ungrounded, it **abstains**.

```text
START -> plan -> retrieve -> answer -> groundedness_check
                    ^                        |
                    +--- retry (max 2 attempts)
                                             +-> END (grounded or abstain)
```

## How the evaluation works

The eval set (`evals/cases.jsonl`) is **18 hand-labeled cases**:

- **12 answerable cases** — a question, the document that should be
  retrieved (`expected_doc`), and the terms a correct answer must
  contain (`expected_terms`).
- **6 abstention cases** — questions the corpus cannot answer
  (cooking, weather, stock prices, sports, travel, home repair). The
  correct behavior is to refuse.

Each case is scored on independent sub-checks, so a failure names the
stage that broke:

| Sub-check | What it measures |
|---|---|
| Retrieval | Expected document appears among the retrieved passages |
| Answer quality | Agent answered (no abstention), answer contains an expected term |
| Groundedness | Every answer sentence passes the overlap check |
| Abstention | Out-of-corpus questions are refused, not invented |

`evals/run_eval.py` prints a PASS/FAIL line per case with a
plain-language diagnosis (e.g. *"retrieval missed expected doc
'11-retrievers' (got: …)"*, *"2 answer sentence(s) failed the
groundedness check (lowest overlap 0.21)"*) and writes a full JSON
report with `--json`.

### Threshold tuning

The groundedness threshold is the system's core trade-off: lower it
and more answers pass (fewer abstentions, more risk); raise it and the
agent refuses more (safer, less useful). `evals/tune_threshold.py`
sweeps the threshold from 0.20 to 0.60 across the whole labeled set so
the default (0.35) is chosen from measurements. In the current
offline configuration the curve is flat — the extractive composer
copies sentences from passages, so overlap is near 1.0 and every
threshold in the swept range passes. The knob starts to bite with the
optional provider composer, whose abstractive answers genuinely vary
in overlap; the harness measures both modes identically.

## Results (verified run)

`python evals/run_eval.py` at the default threshold (0.35), offline
mode, Python 3.12:

| Metric | Result |
|---|---|
| Overall accuracy | **18 / 18 (100%)** |
| Answerable cases passed | 12 / 12 |
| Retrieval hit rate (expected doc retrieved) | 100% |
| Abstention correctness (out-of-corpus refused) | 6 / 6 |
| Threshold sweep 0.20–0.60 | 100% overall at every step (flat — see note above) |
| Smoke tests (`python -m unittest discover tests`) | 2 passed |

The full machine-readable report from this run is committed at
`evals/results/latest.json`, and a recorded single-question run with
sources and per-sentence groundedness scores is in
`tests/expected_run.md`. Reproduce everything with the commands below
— the numbers above are exactly what the harness prints.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Ask one question (offline, no key needed)
python run_agent.py "How do interrupts support human-in-the-loop patterns in LangGraph?"
python run_agent.py "What is the best recipe for banana bread?"   # -> abstains

# Run the labeled evaluation
python evals/run_eval.py                  # per-case PASS/FAIL + diagnosis
python evals/run_eval.py --json evals/results/latest.json
python evals/tune_threshold.py            # threshold trade-off sweep

# Smoke tests
python -m unittest discover tests
```

Configuration is environment-only (see `.env.example`): corpus
directory, grounding threshold, and the optional provider key. No
secrets live in the code.

## Repository layout

```text
run_agent.py            CLI entry point (one run command)
src/agent.py            LangGraph state machine (4 nodes + conditional edge)
src/retrieval.py        Chunking + hybrid BM25 / TF-IDF retrieval
corpus/                 16 public documentation notes + ATTRIBUTION.md
evals/cases.jsonl       18 labeled cases (12 answerable, 6 abstention)
evals/run_eval.py       Eval harness: per-case verdicts + diagnosis + summary
evals/tune_threshold.py Grounding-threshold sweep across the labeled set
evals/results/          Committed JSON report from the verified run
tests/test_agent.py     Smoke tests (grounded answer + abstention)
tests/expected_run.md   Recorded real run with sources visible
```

## What this demonstrates

- **RAG pipelines** — document ingestion, paragraph chunking with
  overlap, hybrid keyword + vector-style retrieval with score
  normalization, relevance gating, and source-carrying results.
- **Evaluation frameworks** — a labeled eval set with independent
  sub-checks per pipeline stage, per-case pass/fail diagnosis that
  localizes failures, and a committed results artifact for regression
  comparison.
- **LLM reliability** — groundedness self-verification, retry with a
  widened retrieval pass, and abstention as a first-class outcome
  instead of a confident hallucination.
- **Threshold tuning** — the abstain/answer trade-off measured across
  a swept parameter range rather than set by intuition.
- **Agent orchestration** — an explicit LangGraph state machine
  (typed state, four nodes, a conditional retry edge) rather than a
  prompt chain.

## Provenance

Packaged from the author's LangGraph retrieval-agent project; the
agent core (`src/agent.py`, `src/retrieval.py`) is unchanged in
behavior, with the grounding threshold and corpus path made
configurable so the harness can sweep them. The corpus is public
documentation notes, attributed in `corpus/ATTRIBUTION.md`. Nothing
private — no employer code, data, or credentials — is in this repo.

## License

MIT — see `LICENSE`. Corpus documents remain under their original
terms; see `corpus/ATTRIBUTION.md`.
