Source: LangGraph documentation - Graph API: nodes and edges (docs.langchain.com/oss/python/langgraph/graph-api)
License: see corpus/ATTRIBUTION.md

# Nodes and Edges

Nodes are functions that perform one unit of work in a graph, such as calling a model, running a tool, retrieving documents, or checking an answer. A node takes the current state as input and returns a dictionary of state updates.

Edges connect nodes and define the order of execution. A normal edge always moves execution from one node to the next node in sequence.

Conditional edges route execution based on the current state. A routing function reads the state and returns the name of the next node, which makes loops, retries, and branching possible inside a single graph.

The special START and END entries mark where execution enters and leaves the graph. A graph must be compiled before it can be invoked, and compilation validates that nodes and edges are connected correctly.
