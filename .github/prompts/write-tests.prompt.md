---
mode: agent
description: Write tests for a named module in rag-evaluation-harness
---

Write tests for the module I name, following this repo's existing test
style, layout, and fixtures. Cover the behavior the module documents,
including these invariants where they apply:

- Never tune the agent and the harness thresholds in the same change — that destroys the measurement.
- A correct abstention scores as a pass, not a failure; groundedness is scored per sentence against a single retrieved passage.
- Labeled cases are data with intent: changing an expected label or expected source requires a stated reason.

Then run the test suite:

    python -m unittest discover tests
python run_agent.py   # agent + harness over the labeled cases

Show the result. Do not claim done unless the suite is green; if a
test cannot pass, say why instead of weakening the assertion.
