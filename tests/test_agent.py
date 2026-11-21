"""Smoke tests: the graph answers a grounded question and abstains on
an out-of-corpus question. Run: python -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from agent import run_agent  # noqa: E402


class TestAgent(unittest.TestCase):
    def test_grounded_answer(self):
        result = run_agent("What is a state graph in LangGraph and how does state flow through it?")
        self.assertTrue(result["hits"], "expected retrieved passages")
        self.assertTrue(result["grounded"], f"expected grounded answer, got: {result['answer']}")
        self.assertIn("state", result["answer"].lower())

    def test_abstains_out_of_corpus(self):
        result = run_agent("What is the best recipe for banana bread?")
        self.assertIn("abstaining", result["answer"])


if __name__ == "__main__":
    unittest.main()
