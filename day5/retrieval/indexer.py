from openai.types.shared import metadata
from config import SAMPLE_DOCS


def load_corpus(docs_path: str | None):
    from langchain_core.documents import Document

    if not docs_path:
        return [Document(page_content=text, metadata={"sources": stc}) for text, src in SAMPLE_DOCS]

    from pathlib import Path
    root = Path(docs_path)

    files = [p for p in root.rglob("*") if p.suffix.lower() in {".md", ".txt"}]

    if not files:
        raise SystemExit(f"No .md/.txt files found under {docs_path}")

    return [
        Document(
            page_content=p.read_text(encoding="utf-8", errors="ignore"),
            metadata={
                "sources": str(p.relative_to(root))
            },
        ) for p in files
    ]

def chunk_docs(docs, chunk_size: int = 500, chunk_overlap: int = 80):
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    ).split_documents(docs)

def build_vectorstore(chunks, embeddings):
    from langchain_community.vectorstores import FAISS
    return FAISS.from_documents(chunks, embeddings)