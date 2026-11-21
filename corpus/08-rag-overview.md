Source: LangChain documentation - Retrieval-Augmented Generation (docs.langchain.com/oss/python/langchain/rag)
License: see corpus/ATTRIBUTION.md

# Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation is a technique that grounds a language model's answer in external documents. Instead of answering from memory alone, the system first retrieves relevant passages and then composes the answer from those passages.

A typical RAG pipeline has two phases. In the indexing phase, documents are loaded, split into chunks, converted into embeddings, and stored in a vector store. In the retrieval phase, the user question is embedded, similar chunks are fetched, and the answer is generated using those chunks as context.

RAG reduces hallucination because the model can be instructed to answer only from retrieved material and to cite the passages it used.

Retrieval quality decides answer quality. If the retriever returns the wrong passages, even a strong model will produce a wrong or unsupported answer, so chunking and search strategy deserve as much attention as the prompt.
