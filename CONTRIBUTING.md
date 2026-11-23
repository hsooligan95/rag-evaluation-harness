# Contributing

Thanks for your interest in **rag-evaluation-harness**. This repository is one component of a
multi-repo agent-governance platform whose components share a single trace
spine ([agent-trace](https://github.com/hsooligan95/agent-trace)). The full
picture is in the [platform guide](https://github.com/hsooligan95/hsooligan95/blob/main/PLATFORM-GUIDE.md).

## Development setup

Python 3.12 (matches CI). Then:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Run the tests

```bash
python -m unittest discover tests
```

All tests must pass before a change is proposed. Report the result the test
run actually produced — never a result it did not.

## Proposing changes

1. Open an issue first for anything larger than a typo fix.
2. Keep changes small and scoped to this repo's one job in the platform.
3. Open a pull request against `main` and fill in the PR template.

## Ground rules

- No secrets in code, tests, fixtures, or examples — placeholders only.
- Preserve the invariants stated in this repo's README. If a change must
  break one, call it out explicitly in the pull request.
