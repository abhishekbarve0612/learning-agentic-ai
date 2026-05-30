FORMAT: what broke → root cause → the fix

When used openai client, the wrapper didn't work -> It gave AttributeError: OpenAI object has no attribute 'messages' -> Fix: Changed to Anthropic client, or could update code to use client.ChatCompletion.create(**kwargs).

When tried 1.5 temperature with Haiku model it gave 400 -> temperature range varies per model, for haiku it ranges between 0 and 1.0 -> reverted to 1.0 worked