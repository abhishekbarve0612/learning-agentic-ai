from config import (
    ANTHROPIC, OPENAI, GOOGLE,
    ANTHROPIC_MODEL, OPENAI_MODEL, GOOGLE_MODEL,
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

    raise ValueError(f"Invalid provider: {provider}, Supported Providers: {ANTHROPIC}, {OPENAI}, {GOOGLE}")
