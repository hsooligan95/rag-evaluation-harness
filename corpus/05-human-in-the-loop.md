Source: LangGraph documentation - Human-in-the-loop (docs.langchain.com/oss/python/langgraph/human-in-the-loop)
License: see corpus/ATTRIBUTION.md

# Human-in-the-Loop

Human-in-the-loop patterns let a person review, approve, or edit an agent's work before the agent continues. LangGraph supports this with interrupts, which pause graph execution at a chosen point and wait for external input.

When a graph interrupts, its state is persisted by the checkpointer, so the pause can last seconds or days. Resuming supplies the human's decision as a command, and execution continues from the exact node where it paused.

Typical uses include approving a tool call before it runs, reviewing a draft answer before it is sent, and collecting missing information from the user mid-task.

Interrupts make agent behavior safer for actions that are expensive, irreversible, or sensitive, because a human stays in control of those steps.
