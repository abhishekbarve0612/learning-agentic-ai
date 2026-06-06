from typing import Callable
from langchain_core.output_parsers import StrOutputParser

from day5.prompts.hyde import HYDE_PROMPT


def make_hyde_gen_chain(llm) -> Callable[[str], str]:
    chain = HYDE_PROMPT | llm | StrOutputParser()

    def hyde(question):
        return chain.invoke({
            "question": question,
        }).strip()

    return hyde