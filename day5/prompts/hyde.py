from langchain_core.prompts import ChatPromptTemplate


HYDE_PROMPT = ChatPromptTemplate.from_template(
    "Write a short, factual-sounding paragraph that directly answers the question, "
    "as if it were an excerpt from an internal company document.\n"
    "Invent plausible-sounding specifics if needed - tone and structure matter more "
    "than factual accuracy.\n\n"
    "Question: {question}\n"
    "Document excerpt:"
)
