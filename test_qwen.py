import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY", "sk-e2099285253b4768893115c95b67b60e")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")

resp = openai.ChatCompletion.create(
    model="qwen-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
)

print(resp["choices"][0]["message"]["content"]) 