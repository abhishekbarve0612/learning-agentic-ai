from typing import Callable
from langchain_core.output_parsers import StrOutputParser

from day5.prompts.step_back import STEP_BACK_PROMPT


def make_step_back_chain(llm) -> Callable[[str], str]:
    chain = STEP_BACK_PROMPT | llm | StrOutputParser()

    return lambda question: chain.invoke({
        "question": question
    }).strip()