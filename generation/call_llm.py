from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from config import BASE_URL, LLM_MODEL

# Point to your server LLAMA endpoint
print(LLM_MODEL)
print(BASE_URL)
llm = Ollama(
    model=LLM_MODEL,     
    base_url=BASE_URL,
    request_timeout=300,  
    temperature=0
)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    messages = [
        ChatMessage(
            role="system", content=system_prompt
        ),
        ChatMessage(role="user", content=user_prompt),
    ]
    resp = llm.chat(messages)
    print(resp)
    return resp.message.content