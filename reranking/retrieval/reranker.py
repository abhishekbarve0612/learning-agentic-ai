from langchain_classic.retrievers.document_compressors import CrossEncoderReranker

def build_reranker(cross_encoder, top_n: int) -> CrossEncoderReranker:
    """Wrap a cross encoder model as a langchain document compressor"""
    return CrossEncoderReranker(model=cross_encoder, top_n=top_n)