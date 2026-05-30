from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# client = OpenAI()
client = Anthropic()

GPT_MINI = "gpt-5.5-mini"
HAIKU = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-4-6"

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