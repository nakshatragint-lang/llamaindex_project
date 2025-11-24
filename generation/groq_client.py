# generation/groq_client.py
import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

def call_groq(system_prompt: str, user_prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0
    }

    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=30
    )

    data = resp.json()

    if "error" in data:
        raise Exception(f"Groq Error: {data['error']}")

    return data["choices"][0]["message"]["content"]
