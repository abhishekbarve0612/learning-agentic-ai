import config


def get_embeddings():
    name = config.EMBED_MODELS[config.EMBED_PROVIDER]

    if config.EMBED_PROVIDER == config.HUGGINGFACE:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=name)
    if config.EMBED_PROVIDER == config.GOOGLE:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(model=name)
    if config.EMBED_PROVIDER == config.OPENAI:
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=name)
    raise ValueError(f"Unknown EMBED_PROVIDER: {config.EMBED_PROVIDER}")

def get_cross_encoder():
    from langchain_community.cross_encoders import HuggingFaceCrossEncoder
    return HuggingFaceCrossEncoder(model_name=config.CROSS_ENCODER_MODEL)

def get_llm():
    provider = config.LLM_PROVIDER
    if provider == "none":
        return None
    model = config.LLM_MODELS[provider]
    if provider == config.OPENAI:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model, temperature=0.0)
    
    if provider == config.ANTHROPIC:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=model, temperature=0.0)

    if provider == config.GOOGLE:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model, temperature=0.0)

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")
