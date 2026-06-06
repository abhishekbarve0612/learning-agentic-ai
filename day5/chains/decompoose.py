from typing import Callable
from langchain_core.output_parsers import StrOutputParser

from day5.prompts.decompose import DECOMPOSE_PROMPT
from day5.utils import _parse_lines


def make_decompose_chain(llm) -> Callable[[str], list[str]]:
    chain = DECOMPOSE_PROMPT | llm | StrOutputParser()

    return lambda question: _parse_lines(chain.invoke({
        "question": question
    }))
