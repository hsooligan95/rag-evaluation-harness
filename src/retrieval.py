"""Hybrid retrieval over the local document corpus.

Two scorers, standard library only:
- Keyword: BM25 over tokenised chunks.
- Vector-lite: TF-IDF vectors with cosine similarity (a transparent,
  dependency-free stand-in for embedding search; swapping in real
  embeddings only changes `TfidfIndex.vectorise`).

Scores are min-max normalised per query and blended 50/50.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "in", "on",
    "of", "to", "and", "or", "for", "with", "how", "what", "when", "which",
    "does", "do", "it", "its", "this", "that", "you", "can", "as", "at",
    "by", "from", "an", "into", "than", "then", "so",
}


def tokenise(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


@dataclass
class Chunk:
    doc_id: str
    source: str
    index: int
    text: str
    tokens: list[str]


@dataclass
class Hit:
    chunk: Chunk
    score: float
    keyword_score: float
    vector_score: float


def chunk_text(text: str, max_chars: int = 700, overlap: int = 120) -> list[str]:
    """Split on paragraph boundaries, packing paragraphs into chunks."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        if current and len(current) + len(para) + 2 > max_chars:
            chunks.append(current)
            current = current[-overlap:] + "\n\n" + para if overlap else para
        else:
            current = current + "\n\n" + para if current else para
    if current:
        chunks.append(current)
    return chunks


class HybridIndex:
    def __init__(self, docs_dir: Path):
        self.chunks: list[Chunk] = []
        for path in sorted(docs_dir.glob("*.md")):
            raw = path.read_text(encoding="utf-8")
            source = path.stem
            for line in raw.splitlines():
                if line.startswith("Source:"):
                    source = line.split("Source:", 1)[1].strip()
                    break
            for i, piece in enumerate(chunk_text(raw)):
                self.chunks.append(
                    Chunk(doc_id=path.stem, source=source, index=i,
                          text=piece, tokens=tokenise(piece))
                )
        self._build()

    def _build(self) -> None:
        n = len(self.chunks)
        self.avg_len = sum(len(c.tokens) for c in self.chunks) / max(n, 1)
        df: dict[str, int] = {}
        for c in self.chunks:
            for tok in set(c.tokens):
                df[tok] = df.get(tok, 0) + 1
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}
        self.vectors: list[dict[str, float]] = []
        self.norms: list[float] = []
        for c in self.chunks:
            vec = self._tfidf(c.tokens)
            self.vectors.append(vec)
            self.norms.append(math.sqrt(sum(v * v for v in vec.values())) or 1.0)

    def _tfidf(self, tokens: list[str]) -> dict[str, float]:
        if not tokens:
            return {}
        counts: dict[str, int] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        return {t: (c / len(tokens)) * self.idf.get(t, 0.0) for t, c in counts.items()}

    def _bm25(self, query_tokens: list[str], chunk: Chunk) -> float:
        k1, b = 1.5, 0.75
        freq: dict[str, int] = {}
        for t in chunk.tokens:
            freq[t] = freq.get(t, 0) + 1
        denom_norm = 1 - b + b * (len(chunk.tokens) / max(self.avg_len, 1))
        score = 0.0
        for t in set(query_tokens):
            f = freq.get(t, 0)
            if f:
                score += self.idf.get(t, 0.0) * (f * (k1 + 1)) / (f + k1 * denom_norm)
        return score

    def search(self, query: str, top_k: int = 4) -> list[Hit]:
        qtokens = tokenise(query)
        qvec = self._tfidf(qtokens)
        qnorm = math.sqrt(sum(v * v for v in qvec.values())) or 1.0
        raw: list[tuple[Chunk, float, float]] = []
        for i, chunk in enumerate(self.chunks):
            kw = self._bm25(qtokens, chunk)
            dot = sum(qvec.get(t, 0.0) * v for t, v in self.vectors[i].items())
            vec = dot / (qnorm * self.norms[i])
            raw.append((chunk, kw, vec))

        def normalise(values: list[float]) -> list[float]:
            hi = max(values) if values else 0.0
            return [v / hi if hi > 0 else 0.0 for v in values]

        kws = normalise([r[1] for r in raw])
        vecs = normalise([r[2] for r in raw])
        hits = [
            Hit(chunk=r[0], score=0.5 * k + 0.5 * v, keyword_score=r[1], vector_score=r[2])
            for r, k, v in zip(raw, kws, vecs)
        ]
        hits.sort(key=lambda h: h.score, reverse=True)
        # Relevance gate: a hit must share at least two distinct query
        # tokens with the chunk. One shared word (e.g. "best") is not
        # evidence the passage is about the question.
        gated = [
            h for h in hits
            if h.score > 0 and len(set(qtokens) & set(h.chunk.tokens)) >= 2
        ]
        return gated[:top_k]
