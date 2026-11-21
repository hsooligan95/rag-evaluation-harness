Source: LangGraph documentation - Persistence (docs.langchain.com/oss/python/langgraph/persistence)
License: see corpus/ATTRIBUTION.md

# Persistence and Checkpointing

LangGraph persistence saves graph state at every step using checkpointers. A checkpointer stores a snapshot of the state after each node runs, tied to a thread identifier that identifies one conversation or run.

Checkpointing enables several capabilities. A run can be resumed after a failure, a human can inspect and modify state before the graph continues, and a conversation can keep its history across separate invocations on the same thread.

Common checkpointer backends include an in-memory saver for development and database-backed savers for production use.

Time travel is also possible: because every step is checkpointed, execution can be replayed or forked from an earlier checkpoint to explore a different path.
