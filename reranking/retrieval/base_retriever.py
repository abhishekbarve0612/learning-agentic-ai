from typing import Any, Sequence

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS


def build_vectorstore(docs: Sequence[Document], embeddings) -> FAISS:
    """Embed every chunk once and build an in-memory FAISS index"""
    return FAISS.from_documents(list[Any](docs), embeddings)

def build_base_retriever(vectorstore: FAISS, k: int):
    """
    The NET: return top-k roughly relevant chunks for any query.
    """
    return vectorstore.as_retriever(search_kwargs={"k": k})