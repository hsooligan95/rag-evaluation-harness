Source: LangGraph documentation - Memory (docs.langchain.com/oss/python/langgraph/memory)
License: see corpus/ATTRIBUTION.md

# Memory: Short-Term and Long-Term

Short-term memory in LangGraph is the state kept inside a single thread. It usually holds the conversation history and intermediate results, and it is persisted automatically when a checkpointer is configured.

Long-term memory stores information across different threads and sessions, such as user preferences and facts learned in earlier conversations. It is kept in a separate store that nodes can read from and write to during a run.

Keeping the two kinds of memory separate matters for design. Short-term memory answers what is happening in this conversation right now, while long-term memory answers what the system knows about this user or domain in general.

Memory updates should be deliberate. Writing everything a model produces into long-term memory pollutes future runs, so production systems usually filter or summarize what gets stored.
