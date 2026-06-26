from langchain_classic.retrievers.document_compressors import (
    DocumentCompressorPipeline, EmbeddingsFilter, LLMChainExtractor
)


def build_embeddings_filter(embeddings, threshold: float) -> EmbeddingsFilter:
    """Fast, local sentence filter. Drops sentences below the cosine sim threshold"""
    return EmbeddingsFilter(
        embeddings=embeddings,
        similarity_threshold=threshold
    )

def build_llm_extractor(llm) -> LLMChainExtractor:
    """Precise sentence exxtractor, one llm call per chunk"""
    if llm is None:
        raise ValueError(
            "COMPRESSION_MODE:'llm_extractor' needs an LLM, but LLM_PROVIDER='none'."
            "Set an LLM provider, or use 'embeddings_filter'"
        )

    return LLMChainExtractor.from_llm(llm)

def build_compressor(reranker, *, mode: str, embeddings=None, llm=None, threshold: float = 0.3):
    if mode == "none":
        return reranker
    if mode == "embeddings_filter":
        laser = build_embeddings_filter(embeddings, threshold)
    elif mode == "llm_extractor":
        laser = build_llm_extractor(llm)
    else:
        raise ValueError(f"Unknown COMPRESSION_MODE: {mode}")
    return DocumentCompressorPipeline(transformers=[reranker, laser])