from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI()
client = Anthropic()

GPT_MINI = "gpt-5.4-mini"
HAIKU = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-4-6"
FLASH = "gemini-3.5-flash"
EMBED_MODEL = "gemini-embedding-001"

def call(
    prompt = None,
    *,
    system = None,
    model = HAIKU,
    temperature = 1.0,
    max_tokens = 1024,
    tools = None,
    messages = None
):
    """Thin wrapper. Returns the full message object (use .content, .usage .stop_reason)"""
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    if system:
        kwargs["system"] = system

    if tools:
        kwargs["tools"] = tools

    kwargs["messages"] = messages if messages is not None else [
        {
            "role": "user", "content": prompt,
        }
    ]

    return client.messages.create(**kwargs)

def text_of(msg):
    """Concatenate all text blocks of a message into a plain sring."""
    return "".join(b.text for b in msg.content if b.type == "text")

def openai_call(
    prompt = None,
    *,
    system = None,
    model = GPT_MINI,
    temperature = 1.0,
    max_tokens = 1024,
    tools = None,
    messages = None
    ):
    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if system:
        kwargs["system"] = system

    if tools:
        kwargs["tools"] = tools

    kwargs["messages"] = messages if messages is not None else [
        {
            "role": "user", "content": prompt,
        }
    ]
    return openai_client.chat.completions.create(**kwargs)

def openai_text_of(msg):
    return "".join(txt for txt in msg.choices[0].message.content)