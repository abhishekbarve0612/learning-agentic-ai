from langchain_core.prompts import ChatPromptTemplate


STEP_BACK_PROMPT = ChatPromptTemplate.from_template(
    "Rephrase the following specific question into a broader, more general quesiton "
    "that is likely to be answered by foundational reference material.\n"
    "Strip hyper-specific entities (dates, branch names, exact percentages) while "
    "keeping the core topic. Return ONLY the rephrased question.\n\n"
    "Original question: {question}"
)
