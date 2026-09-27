from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 900,
    chunk_overlap: int = 150,
) -> list[Document]:
    """Recursive, metadata-preserving chunking.

    Metadata-aware chunking means source filename/page metadata stays attached to
    every chunk, which is required later for traceable citations.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk-{index + 1}"
    return chunks
