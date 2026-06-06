
from typing import Callable
from langchain_core.output_parsers import StrOutputParser

from day5.prompts.math import MATH_PROMPT


def make_math_chain(llm) -> Callable[[str], str]:
    chain = MATH_PROMPT | llm | StrOutputParser()

    return lambda question: chain.invoke({
        "question": question,
    })