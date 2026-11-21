Source: LangChain documentation - Document loaders and text splitters (docs.langchain.com/oss/python/langchain/retrieval)
License: see corpus/ATTRIBUTION.md

# Document Loaders, Splitting, and Chunking

Document loaders read content from sources such as files, web pages, and databases and convert each source into a standard document object with text and metadata, including where the text came from.

Text splitters divide long documents into chunks that are small enough to embed and retrieve precisely. A common strategy splits on natural boundaries such as paragraphs first, then falls back to smaller units when a piece is still too long.

Chunk size and chunk overlap are the two main tuning knobs. Smaller chunks retrieve more precisely but can lose context, while overlap repeats a small part of the previous chunk so an idea that spans a boundary is not cut in half.

Metadata should travel with every chunk. Keeping the source name and position on each chunk is what makes citations and source display possible later in the pipeline.
