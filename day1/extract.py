from pydantic import ConfigDict
import json
from typing import Optional, Literal
from pydantic import BaseModel, ValidationError

from llm import client, text_of, HAIKU
from inputs import INPUTS

class Ticket(BaseModel):

    model_config = ConfigDict(extra="forbid")

    intent: Literal['refund', 'complaint', 'question', 'payment_issue', 'unknown']
    order_id: Optional[str] = None
    amount: Optional[float] = None
    sentiment: Literal['positive', 'negative', 'neutral']


SYSTEM_PROMPT = """
    You extract structured data ffrom customer support messages.
    Output a JSON object with exactly these fields:
    - intent: one of "refund", "complaint", "question", "payment_issue", "unknown"
    - order_id: the order ID as a string, or null if none is mentioned
    - amount: the monetary amount as a number (no currency symbol), or null if none
    - sentiment: one of "positive", "negative", "neutral"

    Rules:
    - Use null when a ield is genuinely absent. NEVER invent an order_id or amount.
    - If the message has no usable content, intent is "unknown".
    - Reply with ONLY the raw JSON object. Do NOT wrap it in markdown code fences or ```json blocks. No backticks, no commentary.
"""

def extract_manual(text: str) -> Ticket:
    msg = client.messages.create(
        model=HAIKU,
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[
            {
                'role': 'user', 'content': f'Message: {text}'
            }
        ],
    )
    print("DEBUG content blocks", msg.content)
    print("DEBUG stop_reason: ", msg.stop_reason)
    raw = text_of(msg).strip()

    print("DEBUG raw: ", repr(raw))

    data = json.loads(raw)
    return Ticket(**data)

def extract_structured(text: str) -> Ticket:
    msg = client.messages.create(
        model=HAIKU,
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[
            { 'role': 'user', 'content': f'Message: {text}'}
        ],
        output_config = {
            'format': {
                'type': 'json_schema',
                'schema': Ticket.model_json_schema()
            }
        },
    )

    raw = text_of(msg)

    return Ticket(**json.loads(raw))

def run(extractor, label):
    print(f"\n=== {label} ===")
    ok = 0
    for input in INPUTS:
        try:
            tk = extractor(input)
            if input.strip() == "" and tk.order_id:
                print(f"FAIL (invented order on empty): {t[:30]!r} {tk.model_dump()}")
                continue
            print(f"OK {repr(input)[:40].ljust(42)} {tk.model_dump()}")
            ok += 1
        except Exception as e:
            print(f"FAIL {repr(input)[:40].ljust(42)} {e} {type(e).__name__}")

    print(f"{ok} / {len(INPUTS)} valid")

if __name__ == '__main__':
    # run(extract_structured, "Version A")
    run(extract_manual, "Version B")