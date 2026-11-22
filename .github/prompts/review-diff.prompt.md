---
mode: agent
description: Review the current diff against rag-evaluation-harness's invariants
---

Review my current diff against this repo's invariants:

- Never tune the agent and the harness thresholds in the same change — that destroys the measurement.
- A correct abstention scores as a pass, not a failure; groundedness is scored per sentence against a single retrieved passage.
- Labeled cases are data with intent: changing an expected label or expected source requires a stated reason.
- All reported numbers must reproduce deterministically; retrieval has a relevance gate (>= 2 distinct query tokens).

Flag every violation with file and line. Also flag any change that
alters a documented behavior contract (output shapes, exit codes,
event schemas, recorded artifacts) without updating the docs and
tests that describe it. No style nitpicks — correctness and contract
violations only.
