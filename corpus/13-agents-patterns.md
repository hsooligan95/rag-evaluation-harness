Source: LangGraph documentation - Agent patterns (docs.langchain.com/oss/python/langgraph/workflows-agents)
License: see corpus/ATTRIBUTION.md

# Agent Patterns: Workflows, Routing, and Reflection

A workflow is a graph where the path is largely decided in advance, while an agent decides more of its own path at runtime. Most production systems mix the two, using fixed steps for predictable work and model decisions only where flexibility is needed.

Routing is a basic pattern: a first node classifies the input and sends it to a specialized node, such as answering from documents, running a calculation, or asking a clarifying question.

The planner-executor pattern separates deciding what to do from doing it. A planner node produces a short plan, executor nodes carry out the steps, and a final node synthesizes the result.

Reflection and self-check patterns add a critic step. After a draft answer is produced, a checker node verifies it against requirements or source material, and the graph loops back to revise when the check fails, or abstains when it cannot fix the problem.
