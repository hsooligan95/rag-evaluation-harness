Source: LangChain documentation - Evaluation concepts (docs.langchain.com)
License: see corpus/ATTRIBUTION.md

# Evaluation and Groundedness

Groundedness means every claim in an answer can be traced back to evidence the system actually retrieved. An answer is grounded when its statements are supported by the passages shown to the model, not merely plausible.

A groundedness check compares each answer sentence against the retrieved passages. Sentences with little or no overlap with any passage are flagged as unsupported, and the system can then revise the answer, retrieve again, or abstain.

Abstaining is a valid and important outcome. When the document set does not contain the answer, saying so is more useful and more trustworthy than inventing a confident response.

Evaluation should be recorded. Saving the question, the retrieved passages, the answer, and the check result for each run creates the evidence needed to compare versions and catch regressions.
