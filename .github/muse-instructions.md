# Copilot instructions — rag-evaluation-harness

You are working in the **RAG Evaluation Harness**: the labeled
evaluation layer for the Factory Floor RAG agent. It measures retrieval
quality, answer groundedness, and abstention behavior over labeled
cases, with per-case diagnosis — answering "should it have answered,
and can every sentence be traced to a retrieved passage?"

## Stack

- Python 3; the system under evaluation is a LangGraph state machine
  over a bundled corpus of 16 documentation notes (see
  `corpus/ATTRIBUTION.md`). Retrieval is standard-library only
  (BM25 + TF-IDF hybrid); answers compose extractively from retrieved
  passages. Fully offline, no API key.

## Tests

```bash
python -m unittest discover tests
python run_agent.py   # run the agent + harness over the labeled cases
```

## Architecture notes

- The harness scores the agent as it finds it. Never tune the agent
  and the harness thresholds in the same change — that destroys the
  measurement.
- Groundedness is per-sentence: the fraction of a sentence's content
  tokens appearing in a single retrieved passage. Below threshold, the
  graph retries once with wider retrieval; still ungrounded, it
  abstains — and a correct abstention scores as a pass, not a failure.
- Labeled cases are data with intent. Changing an expected label or an
  expected source requires a stated reason; silent label edits are
  treated as bugs.
- Retrieval has a relevance gate (a passage must share >= 2 distinct
  query tokens). All reported numbers must reproduce deterministically.

## Shared rules

- Use Unix LF line endings in every file; never CRLF.
- Never commit secrets, tokens, or credentials — real or synthetic-looking.
- Tests must pass before you describe a change as complete; run the test
  command above and report honestly if you cannot.
- Prefer the smallest complete implementation: reuse what already exists in
  this repo before adding new code, files, or dependencies.
