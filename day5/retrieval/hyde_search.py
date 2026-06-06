from typing import Callable

from config import K


def make_hyde_retrieve(
    hyde_gen: Callable[[str], str],
    embeddings,
    vectorstore,
    k: int = K,
) -> Callable[[str], str]:
    def hyde_retrieve(question: str) -> list:
        fake_doc = hyde_gen(question)
        vec      = embeddings.embed_query(fake_doc)

        return vectorstore.similarity_search_by_vector(vec, k=k)

    return hyde_retrieve