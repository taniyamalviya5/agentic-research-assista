# Vector store integrations

The assignment lists ChromaDB, FAISS and Pinecone as RAG vector-store topics.

## ChromaDB — implemented

Used by this project because the assignment's technical requirements explicitly specify ChromaDB.

```python
from langchain_chroma import Chroma

store = Chroma(
    collection_name="research_documents",
    embedding_function=embeddings,
    persist_directory="storage/chroma",
)
```

## FAISS — local alternative

FAISS is useful when you want a local in-process vector index.

```python
from langchain_community.vectorstores import FAISS

store = FAISS.from_documents(documents, embeddings)
results = store.similarity_search("your question", k=5)
```

Trade-off: persistence and metadata lifecycle need to be managed by the application.

## Pinecone — managed alternative

Pinecone is useful when the vector index must be remotely hosted and shared across application instances.

Conceptually:

```python
from langchain_pinecone import PineconeVectorStore

store = PineconeVectorStore(
    index_name="research-documents",
    embedding=embeddings,
)
```

For production, keep the vector-store abstraction behind a repository interface so the rest of the application does not depend on one vendor.

## Selection considerations

| Concern | ChromaDB | FAISS | Pinecone |
|---|---|---|---|
| Local development | Strong | Strong | Requires service |
| Simple persistence | Yes | Application-managed | Managed |
| Distributed service | Limited | No | Yes |
| Assignment requirement | Yes | Topic | Topic |
