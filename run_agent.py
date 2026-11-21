#!/usr/bin/env python3
"""Run the LangGraph retrieval agent.

Usage:
    python run_agent.py "What is a state graph in LangGraph?"
    python run_agent.py            # runs the built-in demo question
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from agent import run_agent  # noqa: E402

DEMO_QUESTION = "What is a state graph in LangGraph and how does state flow through it?"


def main() -> None:
    question = " ".join(sys.argv[1:]).strip() or DEMO_QUESTION
    result = run_agent(question)

    print(f"Question: {question}")
    print(f"Plan: {result.get('plan')}")
    print()
    print("Retrieved passages:")
    for i, hit in enumerate(result.get("hits", []), 1):
        snippet = " ".join(hit.chunk.text.split())[:400]
        print(f"  [{i}] source: {hit.chunk.source} "
              f"(hybrid score {hit.score:.2f})")
        print(f"      {snippet}...")
    print()
    print("Answer:")
    print(f"  {result.get('answer')}")
    print()
    print("Groundedness check:")
    for claim in result.get("claims", []):
        mark = "GROUNDED" if claim["grounded"] else "UNGROUNDED"
        print(f"  [{mark} overlap={claim['overlap']}] {claim['sentence'][:110]}")
    print(f"  Result: {'grounded' if result.get('grounded') else 'ABSTAINED'}")


if __name__ == "__main__":
    main()
