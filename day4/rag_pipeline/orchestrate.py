from dataclasses import dataclass, field
from langchain_core.output_parsers import StrOutputParser

from day4.rag_pipeline.helpers import looks_like_abstention, number_context, parse_cited_ids
from day4.rag_pipeline.prompts import ABSTAIN_MESSAGE
from day4.rag_pipeline.retriever import reorder_for_context


@dataclass
class Answer:
    text: str
    abstained: bool
    cited: list = field(default_factory=list)
    sources: dict = field(default_factory=dict)

def answer_question(question, retriever, llm, prompt):
    docs = retriever.invoke(question)

    if not docs:
        return Answer(ABSTAIN_MESSAGE, abstained=True)
    
    context, sources = number_context(reorder_for_context(docs))

    chain = prompt | llm | StrOutputParser()

    text = chain.invoke({
        "context": context,
        "question": question,
    }).strip()

    if looks_like_abstention(text):
        return Answer(ABSTAIN_MESSAGE, abstained=True)

    return Answer(
        text,
        abstained=False,
        cited=parse_cited_ids(text, sources.keys()),
        sources=sources,
    )

def stream_answer(question, retriever, llm, prompt):
    docs = retriever.invoke(question)

    if not docs:
        yield ABSTAIN_MESSAGE
        return
    
    context, _ = number_context(reorder_for_context(docs))

    for token in (prompt | llm | StrOutputParser()).stream({
        "context": context,
        "question": question,
    }):
        yield token

