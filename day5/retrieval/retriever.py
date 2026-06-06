from config import K


def build_retriever(vectorstore, k: int = K):
    return vectorstore.as_retriever(search_kwargs={"k": k})