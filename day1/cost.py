

from llm import call, text_of, HAIKU, SONNET

PRICES = {
    HAIKU: { 'in': 1.0, 'out': 5.0 },
    SONNET: { 'in': 3.0, 'out': 15.0 },
}

def cost(msg, model) -> float:
    """Returns the USD cost of a single call from its usage."""

    p = PRICES[model]

    input_token_cost = msg.usage.input_tokens * p['in'] / 1e6
    output_token_cost = msg.usage.output_tokens * p['out'] / 1e6

    total_cost = input_token_cost + output_token_cost

    return total_cost

def report(prompt, model = HAIKU):
    msg = call(prompt, model = model, max_tokens = 300)

    print(f'\nprompt ({len(prompt)} chars): {prompt[:50]!r}')
    print('answer: ', text_of(msg)[:80], '...')
    print(f'tokens in/out: {msg.usage.input_tokens} / {msg.usage.output_tokens}')
    print(f'cost: ${cost(msg, model):.6f}')

if __name__ == '__main__':
    report('Hi.')
    report('Explain what an API is in two sentences')
    report('Write a detailed paragraph about the history of the LLM evolutions.')

    # Observations: prompt length plays major part in input tokens, but is not always reliable
    # so should always verify token count using .usage