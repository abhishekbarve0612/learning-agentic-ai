from dataclasses import dataclass
from typing import Any, Callable

from day5.chains.decompoose import make_decompose_chain
from day5.chains.answer import make_answer_chain, make_dual_answer_chain
from day5.chains.hyde import make_hyde_gen_chain
from day5.chains.smalltalk import make_smalltalk_chain
from day5.chains.math import make_math_chain
from day5.chains.planner import make_planner
from day5.chains.step_back import make_step_back_chain
from day5.retrieval.hyde_search import make_hyde_retrieve
from day5.retrieval.indexer import build_vectorstore, chunk_docs, load_corpus
from day5.retrieval.retriever import build_retriever
from day5.schema import Plan, Result, Trace
from day5.utils import _fmt, _sources, _rrf
from providers.embeddings import make_embeddings
from providers.llm import make_llm


@dataclass
class SwitchBoard:
    planner:                 Callable[[str], Plan]
    retriever:               Any
    decompose:               Callable[[str], list[str]]
    step_back_gen:           Callable[[str], str]
    hyde_retrieve:           Callable[[str], list]
    answer:                  Callable[[str, str], str]
    answer_dual:             Callable[[str, str, str], str]
    math:                    Callable[[str], str]
    smalltalk:               Callable[[str], str]

    def route(self, question: str) -> Result:
        plan = self.planner(question)
        
        trace = Trace(question=question, plan=plan, llm_calls=1)

        if plan.route == "smalltalk":
            trace.llm_calls += 1
            return Result(self.smalltalk(question), trace)

        if plan.route == "math":
            trace.llm_calls += 1
            return Result(self.math(question), trace)

        if plan.strategy == "step_back":
            broad                   = self.step_back_gen(question)
            trace.step_back_query   = broad
            trace.llm_calls += 1
            docs_spec               = self.retriever.invoke(question)
            docs_broad              = self.retriever.invoke(broad)
            trace.searches += 1
            trace.candidates        = len(docs_spec) + len(docs_broad)
            trace.llm_calls += 1

            return Result(
                self.answer_dual(_fmt(docs_spec), _fmt(docs_broad), question),
                trace,
            )

        if plan.strategy == "hyde":
            docs                   = self.hyde_retrieve(question)
            trace.searches += 1
            trace.hyde_excerpt     = "(hypothetical document generated)"
            trace.candidates       = trace.kept = len(docs)
            trace.top_sources      = _sources(docs)
            trace.llm_calls += 1

            return Result(
                self.answer(_fmt(docs), question),
                trace
            )

        if plan.strategy == "decompose":
            subs                  = self.decompose(question)
            trace.sub_questions   = subs
            trace.llm_calls += 1
            per_subq              = self.retriever.batch(subs)
            trace.candidates      = sum(len(x) for x in per_subq)
            fused                 = _rrf(per_subq)[:4]
            trace.kept            = len(fused)
            trace.top_sources     = _sources(fused)
            trace.llm_calls += 1

            return Result(
                self.answer(_fmt(fused), question),
                trace,
            )

        docs                 = self.retriever.invoke(question)
        trace.searches += 1
        trace.candidates     = trace.kept = len(docs)
        trace.top_sources    = _sources(docs)
        trace.llm_calls += 1
        
        return Result(
            self.answer(_fmt(docs), question),
            trace,
        )

def build_switchboard(docs_path: str | None = None) -> SwitchBoard:

    llm                = make_llm()
    embedding          = make_embeddings()
    vectorstore        = build_vectorstore(chunk_docs(load_corpus(docs_path)), embedding)

    retriever          = build_retriever(vectorstore)
    hyde_gen           = make_hyde_gen_chain(llm)

    return SwitchBoard(
        planner                  = make_planner(llm),
        retriever                = retriever,
        decompose               = make_decompose_chain(llm),
        step_back_gen            = make_step_back_chain(llm),
        hyde_retrieve            = make_hyde_retrieve(hyde_gen, embedding, vectorstore),
        answer                   = make_answer_chain(llm),
        answer_dual              = make_dual_answer_chain(llm),
        math                     = make_math_chain(llm),
        smalltalk                = make_smalltalk_chain(llm)
    )
