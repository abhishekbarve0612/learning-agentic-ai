from llm import call, text_of

msg = call("Say hello in exactly three words.")

print(text_of(msg))

print("----")

print("tokens in/out: ", msg.usage.input_tokens, "/", msg.usage.output_tokens)