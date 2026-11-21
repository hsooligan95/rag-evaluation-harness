Source: LangGraph documentation - Overview (docs.langchain.com/oss/python/langgraph/overview)
License: see corpus/ATTRIBUTION.md

# LangGraph Overview

LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. It is built by the LangChain team but can be used with or without the rest of the LangChain ecosystem.

LangGraph models an agent as a graph. Nodes are Python functions that do work, edges define how control flows between nodes, and a shared state object is passed along and updated as execution moves through the graph.

The framework is designed for agents that run for many steps, need durable execution, support human-in-the-loop review, and must remember context across steps through short-term and long-term memory.

Because the orchestration is explicit, developers can inspect, interrupt, and resume an agent run instead of treating the agent as a single opaque prompt call.
