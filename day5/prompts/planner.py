from langchain_core.prompts import ChatPromptTemplate


PLANNER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Yiu are a query planner ffor a document-retrieval system."
        "Your job is to classify the user question and choose the best retrieval strategy."
        "Do NOT answer the question, only produce the routing plan. \n\n"
        "Key rule: if the user wants to COMPUTE a value -> math;"
        "if thhey want to LOOJ UP a value from a document -> docs.",
    ),
    ("human", "{question}"),
])