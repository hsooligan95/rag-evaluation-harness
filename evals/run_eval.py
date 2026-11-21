#!/usr/bin/env python3
"""Labeled evaluation harness for the RAG agent.

Runs every case in cases.jsonl through the agent and scores three
things independently, per case:

  retrieval   (answerable cases) the expected document appears among
              the retrieved passages
  answer      (answerable cases) the agent answered (did not abstain),
              the groundedness check passed, and at least one expected
              term appears in the answer
  abstention  (abstention cases) the agent abstained instead of
              inventing an answer to an out-of-corpus question

Every case gets a PASS/FAIL verdict plus a plain-language diagnosis of
which sub-check failed and why, so a failure points at the stage that
broke (retrieval vs. composition vs. grounding) instead of just
lowering a score.

Usage:
    python evals/run_eval.py [--threshold 0.35] [--json out.json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from agent import run_agent  # noqa: E402

CASES_PATH = Path(__file__).resolve().parent / "cases.jsonl"


def load_cases() -> list[dict]:
    return [json.loads(line) for line in
            CASES_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def evaluate_case(case: dict, threshold: float | None = None) -> dict:
    result = run_agent(case["question"], threshold=threshold)
    hits = result.get("hits", [])
    abstained = bool(result.get("abstained") or not result.get("grounded"))
    answer = result.get("answer", "")
    diagnosis: list[str] = []

    if case["kind"] == "abstention":
        passed = abstained
        if passed:
            diagnosis.append("correctly abstained on an out-of-corpus question")
        else:
            diagnosis.append(
                "answered an out-of-corpus question instead of abstaining")
        return {"id": case["id"], "kind": "abstention", "passed": passed,
                "abstained": abstained, "diagnosis": diagnosis}

    # answerable case: three sub-checks
    hit_docs = [h.chunk.doc_id for h in hits]
    retrieval_ok = case["expected_doc"] in hit_docs
    if not retrieval_ok:
        diagnosis.append(
            f"retrieval missed expected doc '{case['expected_doc']}' "
            f"(got: {hit_docs or 'no passages'})")

    terms_found = [t for t in case["expected_terms"]
                   if t.lower() in answer.lower()]
    terms_ok = bool(terms_found) and not abstained
    if abstained:
        diagnosis.append("agent abstained on an in-corpus question")
    elif not terms_found:
        diagnosis.append(
            f"answer contains none of the expected terms "
            f"{case['expected_terms']}")

    ungrounded = [c for c in result.get("claims", []) if not c["grounded"]]
    grounded_ok = bool(result.get("grounded")) and not abstained
    if ungrounded and not abstained:
        worst = min(ungrounded, key=lambda c: c["overlap"])
        diagnosis.append(
            f"{len(ungrounded)} answer sentence(s) failed the groundedness "
            f"check (lowest overlap {worst['overlap']})")

    passed = retrieval_ok and terms_ok and grounded_ok
    if passed:
        diagnosis.append(
            f"retrieved '{case['expected_doc']}', grounded answer "
            f"containing {terms_found}")
    return {"id": case["id"], "kind": "answerable", "passed": passed,
            "retrieval_ok": retrieval_ok, "terms_ok": terms_ok,
            "grounded_ok": grounded_ok, "abstained": abstained,
            "diagnosis": diagnosis}


def run_eval(threshold: float | None = None) -> dict:
    cases = load_cases()
    results = [evaluate_case(c, threshold=threshold) for c in cases]
    ans = [r for r in results if r["kind"] == "answerable"]
    ab = [r for r in results if r["kind"] == "abstention"]
    summary = {
        "cases": len(results),
        "passed": sum(r["passed"] for r in results),
        "answerable": len(ans),
        "answerable_passed": sum(r["passed"] for r in ans),
        "retrieval_hit_rate": (
            sum(r["retrieval_ok"] for r in ans) / len(ans) if ans else 0.0),
        "abstention": len(ab),
        "abstention_correct": sum(r["passed"] for r in ab),
    }
    summary["overall_accuracy"] = summary["passed"] / summary["cases"]
    return {"summary": summary, "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=float, default=None,
                        help="groundedness threshold override")
    parser.add_argument("--json", type=Path, default=None,
                        help="also write the full report to this file")
    args = parser.parse_args()

    report = run_eval(threshold=args.threshold)
    s = report["summary"]
    thr = args.threshold if args.threshold is not None else "default (0.35)"
    print(f"RAG evaluation — {s['cases']} labeled cases "
          f"(grounding threshold: {thr})")
    print("=" * 72)
    for r in report["results"]:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"[{mark}] {r['id']:<22} ({r['kind']})")
        for d in r["diagnosis"]:
            print(f"       - {d}")
    print("=" * 72)
    print(f"Overall:            {s['passed']}/{s['cases']} "
          f"({s['overall_accuracy']:.1%})")
    print(f"Answerable:         {s['answerable_passed']}/{s['answerable']}")
    print(f"Retrieval hit rate: {s['retrieval_hit_rate']:.1%} "
          f"(expected doc in retrieved passages)")
    print(f"Abstention:         {s['abstention_correct']}/{s['abstention']} "
          f"out-of-corpus questions correctly refused")
    if args.json:
        args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nFull report written to {args.json}")


if __name__ == "__main__":
    main()
