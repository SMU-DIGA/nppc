## example: https://github.com/BerriAI/litellm
with open("./api_keys/openai_api_key.txt", "r") as file:
    openai_api_key = file.read().strip()
with open("./api_keys/claude_api_key.txt", "r") as file:
    claude_api_key = file.read().strip()

from litellm import completion

import os

## set ENV variables
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["ANTHROPIC_API_KEY"] = claude_api_key

messages = [{"content": "Hello, how are you?", "role": "user"}]

# openai call
response = completion(model="openai/gpt-4o", messages=messages)
print(response)
# anthropic call
response = completion(model="anthropic/claude-3-sonnet-20240229", messages=messages)
print(response)
