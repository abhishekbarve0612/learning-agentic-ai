import os
from llm import call, text_of, HAIKU
from inputs import INPUTS

CATEGORIES = [
    "refund", "complaint", "question", "payment_issue", "unknown"
]

def v1(msg):
    return f"Categorize this message: {msg}"

def v2(msg):
    return f"Categorize this message {msg} in only these allowed categories: {CATEGORIES}"

def v3(msg):
    return f"""{v2(msg)}.
    
    Definitions of the categories are as follows:
    <definitions>
    refund: request for refund
    complaint: complaint about the service
    question: question about the service
    payment_issue: payment issue
    unknown: unknown category
    </definitions>
    """

def v4(msg):
    return f"""{v3(msg)}
    <examples>
        message: i got two of the same hoodie by mistake
        category: refund

        message: WORST. SERVICE. EVER. been 9 days no delivery #angry order: none idk
        category: complaint

        message: is the blue kurta back in stock?? size M. also do you ship to Pune
        category: question

    </examples>
    Reply with only one category from the list, nothing else.
    If there's no usable content, answer 'unknown'
    """

PROMPTS = {
    "v1": v1,
    "v2": v2,
    "v3": v3,
    "v4": v4
}

def classify(prompt_fn, message):
    raw = text_of(call(prompt_fn(message), model=HAIKU, temperature=0, max_tokens=20))

    return raw.strip().lower()

if __name__ == '__main__':
    for input in INPUTS:
        print(f"input: {input}")
        for fn in PROMPTS.values():
            print(f"{fn.__name__}: {classify(fn, input)}")
        print("-" * 100)