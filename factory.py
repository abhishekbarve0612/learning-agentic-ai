

from config import (
    ANTHROPIC, OPENAI, GOOGLE, HUGGINGFACE,
    ANTHROPIC_MODEL, OPENAI_MODEL, GOOGLE_MODEL,
    HUGGINGFACE_EMBEDDING_MODEL, OPENAI_EMBEDDING_MODEL, GOOGLE_EMBEDDING_MODEL,
    TEMPERATURE,
)


def make_llm(provider=ANTHROPIC, temperature=TEMPERATURE):
    if provider == ANTHROPIC:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=ANTHROPIC_MODEL, temperature=temperature)
    if provider == OPENAI:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=OPENAI_MODEL, temperature=temperature)

    if provider == GOOGLE:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=GOOGLE_MODEL, temperature=temperature)

    raise ValueError(f"Invalid provider: {provider}")

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

    raise ValueError(f"Invalid provider: {provider}")