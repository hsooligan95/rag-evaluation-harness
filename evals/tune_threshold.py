#!/usr/bin/env python3
"""Threshold tuning sweep for the groundedness check.

The groundedness threshold is the trade-off knob of the whole system:
lower it and more answers pass the self-check (fewer abstentions, more
risk of weakly supported answers); raise it and the agent abstains
more (safer, but refuses questions it could have answered). This
script runs the full labeled eval set at each candidate threshold and
prints the trade-off table so the default is chosen from measurements,
not vibes.

Usage:
    python evals/tune_threshold.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_eval import run_eval  # noqa: E402

THRESHOLDS = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]


def main() -> None:
    print(f"{'threshold':>9} | {'answerable':>10} | {'abstention':>10} | "
          f"{'overall':>8}")
    print("-" * 48)
    for thr in THRESHOLDS:
        s = run_eval(threshold=thr)["summary"]
        print(f"{thr:>9.2f} | "
              f"{s['answerable_passed']:>4}/{s['answerable']:<5} | "
              f"{s['abstention_correct']:>4}/{s['abstention']:<5} | "
              f"{s['overall_accuracy']:>7.1%}")


if __name__ == "__main__":
    main()
