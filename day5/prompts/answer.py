from langchain_core.prompts import ChatPromptTemplate


ANSWER_PROMPT = ChatPromptTemplate.from_template(
    "Answer the question using ONLY the context below. "
    "If the answer is not present, say you don't know. \n\n"
    "Context: \n{context}\n\n"
    "Question: {question}\n"
    "Answer:"
)

DUAL_ANSWER_PROMPT = ChatPromptTemplate.from_template(
    "Answer the question using ONLY the context below.\n\n"
    "Foundational context (broad principles from the step-back query): \n {step_back_context}\n\n"
    "Specific context (direct facts for the original question): \n{normal_context}\n\n"
    "Question: {question}\n"
    "Answer:"
)
