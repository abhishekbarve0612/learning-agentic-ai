
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from llm import EMBED_MODEL, FLASH

load_dotenv()


llm = ChatGoogleGenerativeAI(model = FLASH, temperature = 0.0)

embed = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)

docs = [
    Document(
        page_content="The Q4 infrastructure audit was authored by Jaymin Patel, Head of Data Engineering.",
        metadata={ "source": "q4_audit.md" },
    ),
        Document(page_content="The Q4 audit measured an OCR failure rate of 15% across the document ingestion pipeline.",
             metadata={"source": "q4_audit.md"}),
    Document(page_content="The approved Q4 modernization budget is $45,000, signed off by the European division finance lead.",
             metadata={"source": "budget.md"}),
    Document(page_content="Standard Operating Procedure for OCR: scans below 200 DPI cause recognition failures.",
             metadata={"source": "sop_ocr.md"}),
    Document(page_content="Remote-work policy: employees may work remotely up to 3 days/week with manager approval.",
             metadata={"source": "hr_policy.md"}),
]

vectorstore = FAISS.from_documents(docs, embed)
