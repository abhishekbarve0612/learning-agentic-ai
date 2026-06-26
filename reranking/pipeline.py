from typing import Sequence
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_classic.retrievers import ContextualCompressionRetriever

import config
from reranking import providers
from reranking.retrieval.base_retriever import build_base_retriever, build_vectorstore
from reranking.retrieval.compressor import build_compressor
from reranking.retrieval.reranker import build_reranker


RAG_PROMPT = PromptTemplate.from_template(
    """You are an elite MLOps auditing assistant. Answer using ONLY the vetted context.
    If the context does not contain the answer, say you don't have enough information.

    Context:
    {context}

    Question: {question}
    Answer:
    """
)

def format_docs(docs: Sequence[Document]) -> str:
    return "\n\n".join(d.page_content for d in docs)

def build_compression_retriever(docs: Sequence[Document]):
    embeddings = providers.get_embeddings()
    vectorstore = build_vectorstore(docs, embeddings)
    retriever = build_base_retriever(vectorstore, k =config.NET_K)

    reranker = build_reranker(
        providers.get_cross_encoder(),
        top_n=config.RERANK_TOP_K
    )

    compressor = build_compressor(
        reranker,
        mode=config.COMPRESSION_MODE,
        embeddings=embeddings,
        llm=providers.get_llm() if config.COMPRESSION_MODE == "llm_extractor" else None,
        threshold=config.EMBEDDINGS_FILTER_THRESHOLD,
    )

    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=retriever,
    )

def build_rag_chain(compression_retriever, llm):
    return (
        {
            "context": compression_retriever | format_docs, "question": RunnablePassthrough()
        } | RAG_PROMPT | llm | StrOutputParser()
    )
