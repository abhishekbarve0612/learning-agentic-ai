
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

SAMPLE_DOCS: list[tuple[str, str]] = [
    ("Authentication. Orbit uses API keys passed in the 'X-Orbit-Key' header. "
     "OAuth is not supported. Keys are created in the dashboard under Settings > Keys.",
     "auth.md"),
    ("Rate limits. The free tier allows 60 requests per minute. The Pro tier allows "
     "600 requests per minute. Exceeding the limit returns HTTP 429.",
     "limits.md"),
    ("Pagination. List endpoints return at most 100 items per page. Use the 'cursor' "
     "query parameter to fetch the next page; an empty cursor means the last page.",
     "pagination.md"),
    ("Deprecation. The v1 'POST /charge' endpoint is deprecated and will be removed on "
     "2027-01-01. Migrate to 'POST /payments', which replaces it one-to-one.",
     "deprecations.md"),
    ("Webhooks. Orbit signs every webhook with an HMAC-SHA256 signature in the "
     "'X-Orbit-Signature' header. Verify it against your endpoint secret before trusting "
     "the payload. Webhooks retry up to 5 times with exponential backoff.",
     "webhooks.md"),
    ("Regions. Data is stored in the region you select at signup (us-east, eu-west, or "
     "ap-south). Region cannot be changed after signup without contacting support.",
     "regions.md"),
]

DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 80

def load_corpus(docs_path):
    if not docs_path:
        return [Document(page_content=doc, metadata={"source": source }) for doc, source in SAMPLE_DOCS]
    
    root = Path(docs_path)
    
    files = [file for file in root.rglob("*") if file.suffix.lower() in {".md", ".txt"}]

    return [
        Document(page_content=file.read_text(encoding="utf-8", errors="ignore"),
        metadata={ "source": str(file.relative_to(root)) }) for file in files
    ]

def chunk_docs(docs, chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", ", ", " ", ""]
    )

    return splitter.split_documents(docs)
