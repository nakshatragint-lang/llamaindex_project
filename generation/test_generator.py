import json
from .groq_client import call_groq
from config import prompt_rules as system_prompt

def generate_tests(context: str, user_prompt: str) -> dict:
    full_prompt = (
        f"Context:\n{context}\n\n"
        f"User Request:\n{user_prompt}\n\n"
        f"Return ONLY valid JSON. No text outside JSON. "
    )

    try:
        raw = call_groq(system_prompt, full_prompt)

        # Try parsing JSON directly
        return json.loads(raw)

    except json.JSONDecodeError:
        # LLM returned garbage → wrap it so at least pipeline doesn't explode
        return {
            "error": "model_returned_invalid_json",
            "raw_output": raw
        }

    except Exception as e:
        raise RuntimeError(f"generate_tests failed: {e}")

