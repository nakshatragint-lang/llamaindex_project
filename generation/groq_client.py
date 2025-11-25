# generation/groq_client.py
import os
import requests
from llama_index.llms.groq import Groq
from llama_index.core.llms import ChatMessage
from config import GROQ_API_KEY, GROQ_MODEL
print("Using GROQ Model:", GROQ_MODEL)
print()

def call_groq(system_prompt: str, user_prompt: str) -> str:
    # headers = {
    #     "Authorization": f"Bearer {GROQ_API_KEY}",
    #     "Content-Type": "application/json"
    # }

    # payload = {
    #     "model": GROQ_MODEL,
    #     "messages": [
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt}
    #     ],
    #     "temperature": 0
    # }

    # resp = requests.post(
    #     "https://api.groq.com/openai/v1/chat/completions",
    #     json=payload,
    #     headers=headers,
    #     timeout=30
    # )

    # data = resp.json()

    # if "error" in data:
    #     raise Exception(f"Groq Error: {data['error']}")
    # return data["choices"][0]["message"]["content"]
    llm = Groq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
    messages = [
        ChatMessage(
            role="system", content=system_prompt
        ),
        ChatMessage(role="user", content=user_prompt),
    ]
    resp = llm.chat(messages)
    print(resp)
    return resp.message.content