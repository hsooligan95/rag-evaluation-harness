Source: LangGraph documentation - Graph API / StateGraph (docs.langchain.com/oss/python/langgraph/graph-api)
License: see corpus/ATTRIBUTION.md

# StateGraph and State

A StateGraph is the main graph class in LangGraph. You define a graph by declaring a state schema, adding nodes, and connecting them with edges, then compiling the graph into a runnable application.

State is the shared data structure that every node can read and update. The state schema is commonly a typed dictionary that declares the keys the graph works with, such as the user question, a plan, retrieved documents, a draft answer, and check results.

Each node receives the current state and returns a partial update. LangGraph merges that update into the state before the next node runs, so state flows through the graph step by step and every later node sees the work of earlier nodes.

Reducers control how updates to a key are combined. The default behavior replaces the previous value, while other reducers can append to a list, which is how message histories accumulate across steps.
