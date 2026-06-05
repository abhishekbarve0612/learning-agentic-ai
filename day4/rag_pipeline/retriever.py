
TOP_K = 4
SCORE_THRESHOLD = 0.3

def build_retriever(chunks, embeddings, k = TOP_K, score_threshold=SCORE_THRESHOLD):
    from langchain_community.vectorstores import FAISS
    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": k,
            "score_threshold": score_threshold,
        }
    )

def reorder_for_context(chunks):
    from langchain_community.document_transformers import LongContextReorder
    return list(LongContextReorder().transform_documents(chunks))