from langchain_core.prompts import ChatPromptTemplate


MATH_PROMPT = ChatPromptTemplate.from_template(
    "You are  a precise calculator. Solve the following and show every step. \n\n"
    "Question: {question}"
)
