from langchain_core.documents import Document


AUDIT_DOCS = [
    Document(page_content="MLOps Audit Q4: European division legacy branches report a 15% OCR failure rate.", metadata={"id": 1, "role": "needle"}),
    Document(page_content="Tuesday Review confirmed the 15% spike is due to 'Legacy Scan-X' hardware and firmware v2.1.", metadata={"id": 2}),
    Document(page_content="Jaymin approved a $45,000 emergency budget to upgrade European scanners by Q1 end.", metadata={"id": 3}),
    Document(page_content="OCR failures peak on Tuesdays due to weekly bulk-batch processing of handwritten PDFs.", metadata={"id": 4}),
    Document(page_content="Tony recommends a distributed architecture for handling 500+ PDFs in legacy branches.", metadata={"id": 5}),
    Document(page_content="The 15% error rate is classified as 'Critical' for Banking and Compliance audits.", metadata={"id": 6}),
    Document(page_content="Marten's team is monitoring OCR logs 24/7 until the hardware upgrade is finished.", metadata={"id": 7}),
    Document(page_content="European legacy branches are the only units still using the v2.1 firmware.", metadata={"id": 8}),
    Document(page_content="The new firmware v3.0 has been successfully tested in the North American cluster.", metadata={"id": 9}),
    Document(page_content="Budget allocation for Q1 also includes a 10% reserve for unexpected cloud egress costs.", metadata={"id": 10}),
    Document(page_content="Anisha suggested moving OCR processing to an asynchronous queue using RabbitMQ.", metadata={"id": 11}),
    Document(page_content="Legacy Scan-X machines have a known overheating issue when processing over 100 pages.", metadata={"id": 12}),
    Document(page_content="Compliance team noted that OCR errors are leading to incorrect data in customer KYC files.", metadata={"id": 13}),
    Document(page_content="The upgrade project is codenamed 'Project Vision' and is led by the MLOps Core team.", metadata={"id": 14}),
    Document(page_content="Handwritten PDF recognition accuracy dropped to 62% in the last batch test.", metadata={"id": 15}),
    Document(page_content="Security audit found that legacy firmware v2.1 has three unpatched vulnerabilities.", metadata={"id": 16}),
    Document(page_content="Training data for the new OCR model includes 50,000 samples of handwritten European scripts.", metadata={"id": 17}),
    Document(page_content="The hardware vendor 'OptiScan' has been notified about the hardware failures.", metadata={"id": 18}),
    Document(page_content="A temporary patch was deployed on Monday to reduce memory leaks during batch processing.", metadata={"id": 19}),
    Document(page_content="Q2 Roadmap: Complete migration of all legacy branches to the centralized MLOps platform.", metadata={"id": 20}),
]

_FILLER = (
    " The meeting also covered the quarterly offsite schedule, the updated parking "
    "policy, several unrelated team milestones, and a reminder about the cafeteria menu."
)

FAT_AUDIT_DOCS = [
    Document(page_content=d.page_content + _FILLER, metadata=d.metadata) for d in AUDIT_DOCS
]

DEFAULT_QUERY = "What is the exact OCR ffailure rate mentioned in the Q4 audit?"