import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import call, text_of, HAIKU

# PROMPT = "Name a single random fruit. Reply with only the fruit name."
PROMPT = "Write a four-word sentence about the ocean. Reply with only the sentence."

def run_n(temp, n = 5):
    print(f'\n --- temperature = {temp} ---')
    outputs = []

    for _ in range(n):
        out = text_of(call(PROMPT, model = HAIKU, temperature=temp, max_tokens=20)).strip()

        outputs.append(out)
        print(" ", out)

    distinct = len(set(outputs))
    print(f'distint answers: {distinct} / {n}')

if __name__ == '__main__':
    run_n(0.0)
    run_n(1.5)

    # Observations: Low Temperature = deterministic, High Temperature = random
