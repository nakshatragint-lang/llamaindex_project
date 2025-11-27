from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import HF_EMBED_MODEL

def get_embedder():
    return HuggingFaceEmbedding(model_name=HF_EMBED_MODEL)
