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

K = 3
RRF_K = 60



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