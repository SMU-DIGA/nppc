import os
from openai import OpenAI, AsyncOpenAI
import asyncio


def set_api_keys():
    with open("../api_keys/openai_api_key.txt", "r") as file:
        openai_api_key = file.read().strip()
    with open("../api_keys/deepseek_api_key.txt", "r") as file:
        deepseek_api_key = file.read().strip()
    with open("../api_keys/claude_api_key.txt", "r") as file:
        claude_api_key = file.read().strip()
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
    os.environ["ANTHROPIC_API_KEY"] = claude_api_key

    with open("../api_keys/huoshan_api_key.txt", "r") as file:
        huoshan_api_key = file.read().strip()
    os.environ["ARK_API_KEY"] = huoshan_api_key


set_api_keys()
client = OpenAI(
    api_key=os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="deepseek-r1-250120",  # your model endpoint ID
    messages=[
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
print(completion.choices[0].message.content)

print("Done!")
