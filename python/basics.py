def create_prompt(topic):
    return f"Tell me about {topic}"

topics = ["FastAPI", "Pydantic", "Asyncio"]

prompts = [create_prompt(topic) for topic in topics]

print(prompts)