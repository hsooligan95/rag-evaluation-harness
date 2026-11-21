Source: LangChain documentation - Retrievers (docs.langchain.com/oss/python/langchain/retrieval)
License: see corpus/ATTRIBUTION.md

# Retrievers

A retriever is the component that takes a query and returns the documents most relevant to it. In LangChain, retrievers expose a standard interface, so a vector store retriever, a keyword retriever, or a hybrid retriever can be swapped without changing the rest of the application.

The number of returned documents, often called top-k, is a key setting. Returning too few documents risks missing the answer, while returning too many adds noise and cost to the generation step.

Re-ranking is an optional second pass that scores the first set of candidates more carefully and keeps only the best few. It improves precision when the first retrieval stage is broad.

A retriever should return provenance with every result. Source identifiers on each returned document let the answer step cite exactly which passages support each claim.
