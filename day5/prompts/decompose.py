from langchain_core.prompts import ChatPromptTemplate


DECOMPOSE_PROMPT = ChatPromptTemplate.from_template(
    "Break the following question into the MINIMUM number of DISTINCT, standalone "
    "sub-questions needed to answer it fully. \n"
    "Rules:\n"
    "   - One sub-question per line, no numbering or bullets.\n"
    "   - If the question is already single-intent, return it unchanged on one line.\n"
    "   - Each sub-question must be self-contained.\n\n"
    "Question: {question}"
)
