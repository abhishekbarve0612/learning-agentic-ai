from config import (
    OPENAI, GOOGLE, HUGGINGFACE,
    HUGGINGFACE_EMBEDDING_MODEL, OPENAI_EMBEDDING_MODEL, GOOGLE_EMBEDDING_MODEL,
)

def make_embeddings(provider=HUGGINGFACE):
    if provider == HUGGINGFACE:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=HUGGINGFACE_EMBEDDING_MODEL,
            encode_kwargs={"normalize_embeddings": True},
        )

    if provider == OPENAI:
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    if provider == GOOGLE:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)

    raise ValueError(f"Invalid provider: {provider}, valid embedding providers: {HUGGINGFACE}, {OPENAI}, {GOOGLE}")