import os
from dotenv import load_dotenv


ANTHROPIC = "anthropic"
OPENAI = "openai"
GOOGLE = "google"
HUGGINGFACE = "huggingface"
TEMPERATURE = 0.0

ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
OPENAI_MODEL = "gpt-4o"
GOOGLE_MODEL = "gemini-3.5-flash"

HUGGINGFACE_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
GOOGLE_EMBEDDING_MODEL = "gemini-embedding-001"

EMBED_MODELS = {
    HUGGINGFACE: HUGGINGFACE_EMBEDDING_MODEL,
    GOOGLE: GOOGLE_EMBEDDING_MODEL,
    OPENAI: OPENAI_EMBEDDING_MODEL,
}

LLM_MODELS = {
    OPENAI: OPENAI_MODEL,
    ANTHROPIC: ANTHROPIC_MODEL,
    GOOGLE: GOOGLE_MODEL,
}

LLM_PROVIDER = ANTHROPIC
EMBED_PROVIDER = HUGGINGFACE

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

K = 3
RRF_K = 60

NET_K = 15 # How wide the net casts (recall)
RERANK_TOP_K = 3 # How many the scalpel keeps (precision)




load_dotenv()

SAMPLE_DOCS: list[tuple[str, str]] = [
    ("Standard Operating Procedure for OCR: scans below 200 DPI cause character "
     "recognition failures. Always rescan low-resolution documents.",    "sop_ocr.md"),
    ("The Q4 infrastructure audit was authored by Jaymin Patel, Head of Data Engineering.",
                                                                          "q4_audit.md"),
    ("The Q4 audit measured an OCR failure rate of 15% across the document ingestion "
     "pipeline.",                                                          "q4_audit.md"),
    ("The approved Q4 modernization budget is $45,000, signed off by the European "
     "finance lead.",                                                       "budget.md"),
    ("The European division still runs legacy branch-office scanners operating at low DPI.",
                                                                         "europe_ops.md"),
    ("Remote-work policy: employees may work remotely up to 3 days/week with manager "
     "approval.",                                                          "hr_policy.md"),
]

EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "huggingface")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "none")

COMPRESSION_MODE = os.getenv("COMPRESSION_MODE", "embeddings_filter")

EMBEDDINGS_FILTER_THRESHOLD = float(os.getenv("EMB_FILTER_THRESHOLD", "0.3"))
