import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")  # good free Groq model
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL")
CLONE_BASE = os.getenv("CLONE_BASE", "/tmp/repos")
rules_path = os.path.join(os.path.dirname(__file__), "prompt_rules.txt")
prompt_rules = open(rules_path, "r", encoding="utf-8").read()

if not DB_URL:
    raise ValueError("DATABASE_URL must be set in environment.")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY must be set in environment.")
