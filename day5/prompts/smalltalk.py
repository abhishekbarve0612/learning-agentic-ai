from langchain_core.prompts import ChatPromptTemplate


SMALLTALK_PROMPT = ChatPromptTemplate.from_template(
    "Reply warmly and briefly to the following message.  "
    "Do not mention the knowledge base or any documents. \n\n"
    "Message: {question}"
)