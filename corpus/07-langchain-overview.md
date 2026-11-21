Source: LangChain documentation - Overview (docs.langchain.com/oss/python/langchain/overview)
License: see corpus/ATTRIBUTION.md

# LangChain Overview

LangChain is a framework for building applications powered by large language models. It provides standard interfaces for models, prompts, tools, retrievers, and output parsers so components from different providers can be combined.

A central idea in LangChain is composability: small pieces such as a prompt template, a chat model, and a parser are chained into a runnable pipeline with a predictable input and output shape.

LangChain includes integrations for hundreds of model providers, vector stores, document loaders, and tools, which saves the integration work of calling each service directly.

LangGraph is the companion framework for orchestration. LangChain components can be used inside LangGraph nodes when an application needs explicit state, branching, and durable execution.
