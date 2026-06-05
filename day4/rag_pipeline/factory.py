ANTHROPIC = "anthropic"
OPENAI = "openai"
GOOGLE = "google"
HUGGINGFACE = "huggingface"
temperature = 0.0

ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
OPENAI_MODEL = "gpt-4o"
GOOGLE_MODEL = "gemini-3.5-flash"

HUGGINGFACE_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
GOOGLE_EMBEDDING_MODEL = "gemini-embedding-001"

def make_llm(provider=ANTHROPIC, temperature=temperature):
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