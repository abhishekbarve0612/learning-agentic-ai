
from typing import Callable
from langchain_core.output_parsers import StrOutputParser

from day5.prompts.answer import ANSWER_PROMPT, DUAL_ANSWER_PROMPT


def make_answer_chain(llm) -> Callable[[str, str], str]:
    chain = ANSWER_PROMPT | llm | StrOutputParser()

    return lambda context, question: chain.invoke({
        "context": context,
        "question": question,
    })

def make_dual_answer_chain(llm) -> Callable[[str, str], str]:
    chain = DUAL_ANSWER_PROMPT | llm | StrOutputParser()
    return lambda normal, sb_ctx, question: chain.invoke({
        "normal_context": normal,
        "step_back_context": sb_ctx,
        "question": question
    })
