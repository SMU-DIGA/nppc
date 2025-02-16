from litellm import completion
import os

## set ENV variables
os.environ["OPENAI_API_KEY"] = "your-openai-key"
# os.environ["ANTHROPIC_API_KEY"] = "your-cohere-key"

messages = [{"content": "Hello, how are you?", "role": "user"}]

# openai call
response = completion(model="openai/gpt-4o", messages=messages)

# anthropic call
response = completion(model="anthropic/claude-3-sonnet-20240229", messages=messages)
print(response)
