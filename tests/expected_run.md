# Recorded run — 2026-11-18

Command: `python run_agent.py` (built-in demo question, offline, no API key set).
Environment: Python 3.12, langgraph 1.2.22, langchain-core 1.8.2.

```text
Question: What is a state graph in LangGraph and how does state flow through it?
Plan: concept lookup

Retrieved passages:
  [1] source: LangGraph documentation - Graph API / StateGraph (docs.langchain.com/oss/python/langgraph/graph-api) (hybrid score 0.93)
      Source: LangGraph documentation - Graph API / StateGraph (docs.langchain.com/oss/python/langgraph/graph-api) License: see docs/ATTRIBUTION.md # StateGraph and State A StateGraph is the main graph class in LangGraph. You define a graph by declaring a state schema, adding nodes, and connecting them with edges, then compiling the graph into a runnable application. State is the shared data structure t...
  [2] source: LangGraph documentation - Overview (docs.langchain.com/oss/python/langgraph/overview) (hybrid score 0.93)
      Source: LangGraph documentation - Overview (docs.langchain.com/oss/python/langgraph/overview) License: see docs/ATTRIBUTION.md # LangGraph Overview LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. It is built by the LangChain team but can be used with or without the rest of the LangChain ecosystem. LangGraph models an agent as a ...
  [3] source: LangGraph documentation - Graph API / StateGraph (docs.langchain.com/oss/python/langgraph/graph-api) (hybrid score 0.86)
      he keys the graph works with, such as the user question, a plan, retrieved documents, a draft answer, and check results. Each node receives the current state and returns a partial update. LangGraph merges that update into the state before the next node runs, so state flows through the graph step by step and every later node sees the work of earlier nodes. Reducers control how updates to a key are ...
  [4] source: LangGraph documentation - Overview (docs.langchain.com/oss/python/langgraph/overview) (hybrid score 0.70)
      control flows between nodes, and a shared state object is passed along and updated as execution moves through the graph. The framework is designed for agents that run for many steps, need durable execution, support human-in-the-loop review, and must remember context across steps through short-term and long-term memory. Because the orchestration is explicit, developers can inspect, interrupt, and r...

Answer:
  LangGraph merges that update into the state before the next node runs, so state flows through the graph step by step and every later node sees the work of earlier nodes. Nodes are Python functions that do work, edges define how control flows between nodes, and a shared state object is passed along and updated as execution moves through the graph. You define a graph by declaring a state schema, adding nodes, and connecting them with edges, then compiling the graph into a runnable application. The state schema is commonly a typed dictionary that declares the keys the graph works with, such as the user question, a plan, retrieved documents, a draft answer, and check results.

Groundedness check:
  [GROUNDED overlap=1.0] LangGraph merges that update into the state before the next node runs, so state flows through the graph step b
  [GROUNDED overlap=1.0] Nodes are Python functions that do work, edges define how control flows between nodes, and a shared state obje
  [GROUNDED overlap=1.0] You define a graph by declaring a state schema, adding nodes, and connecting them with edges, then compiling t
  [GROUNDED overlap=1.0] The state schema is commonly a typed dictionary that declares the keys the graph works with, such as the user
  Result: grounded
```

## Out-of-corpus check (same day)

Command: `python run_agent.py "What is the best recipe for banana bread?"`

No passage passes the relevance gate, the groundedness check fails, and
the agent abstains instead of inventing an answer:

```text
Question: What is the best recipe for banana bread?
Plan: concept lookup

Retrieved passages:

Answer:
  I could not ground an answer to that question in the document set, so I am abstaining rather than guessing.

Groundedness check:
  Result: ABSTAINED
```

## Tests

`python -m unittest discover tests` — 2 tests, OK (grounded answer +
abstention), run 2026-11-18.
