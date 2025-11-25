from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import HF_EMBED_MODEL
from transformers import AutoTokenizer

def get_embedder():
    return HuggingFaceEmbedding(model_name=HF_EMBED_MODEL)


def get_embedding_dimension():
    """
    Returns the dimension of the embeddings produced by the configured embedder.
    """
    print(f"Using embedding model: {HF_EMBED_MODEL}")
    embedder = get_embedder()
    # Generate a test embedding to determine the dimension
    test_embedding = embedder.get_text_embedding("test")
    print(f"Embedding dimension: {len(test_embedding)}")

# get_embedding_dimension()



# def count_tokens(text: str) -> int:
#     tokenizer = AutoTokenizer.from_pretrained(HF_EMBED_MODEL)
#     tokens = tokenizer.encode(text, add_special_tokens=False)
#     return len(tokens)

# print(count_tokens("public class Example {}"))

def count_embedding_tokens(nodes, tokenizer):
    total = 0
    per_node = []

    for node in nodes:
        text = node.text
        token_count = len(tokenizer.encode(text, add_special_tokens=False))
        per_node.append((node.node_id, token_count))
        total += token_count

    return total, per_node
