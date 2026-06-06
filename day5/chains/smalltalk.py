from typing import Callable
from langchain_core.output_parsers import StrOutputParser

from day5.prompts.smalltalk import SMALLTALK_PROMPT


def make_smalltalk_chain(llm) -> Callable[[str], str]:
    chain = SMALLTALK_PROMPT | llm | StrOutputParser()

    return lambda question: chain.invoke({
        "question": question,
    })
