Source: LangChain documentation - Embeddings and vector stores (docs.langchain.com/oss/python/langchain/retrieval)
License: see corpus/ATTRIBUTION.md

# Embeddings and Vector Stores

An embedding is a list of numbers that represents the meaning of a piece of text. Texts with similar meaning get vectors that point in similar directions, so similarity between texts can be measured with cosine similarity between their vectors.

A vector store indexes embeddings so the closest vectors to a query vector can be found quickly, even across millions of chunks. Popular vector stores include FAISS for local use and managed services such as Pinecone for production.

Semantic search with embeddings finds passages that mean the same thing as the query even when they share few exact words. Its weakness is exact identifiers, error codes, and rare names, where keyword search is often more reliable.

Hybrid search combines both approaches. Keyword scores and vector scores are normalized and blended, which usually retrieves better passages than either method alone.
