import tempfile
from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext, Settings

from .clone import clone_repo
from .extractor import extract_relevant_files
from .chunker import chunk_repo_files
from .embedder import get_embedder
from .vector_store import get_pg_store, get_qdrant_store
from transformers import AutoTokenizer
from config import HF_EMBED_MODEL


def ingest_repo_service(repo_url: str):
    repo_path = clone_repo(repo_url)

    workspace = tempfile.mkdtemp()
    extract_relevant_files(repo_path, workspace)

    # chunking
    nodes = chunk_repo_files(workspace)

    # embedding with BATCHING
    embedder = get_embedder()
    Settings.embed_model = embedder
    
    # Batch embed nodes for MUCH faster processing
    print(f"Embedding {len(nodes)} nodes in batches...")
    BATCH_SIZE = 32  # Adjust based on your memory
    
    for i in range(0, len(nodes), BATCH_SIZE):
        batch = nodes[i:i+BATCH_SIZE]
        texts = [node.text for node in batch]
        embeddings = embedder.get_text_embedding_batch(texts)
        
        for node, emb in zip(batch, embeddings):
            node.embedding = emb
        
        if (i + BATCH_SIZE) % 320 == 0:  # Progress every 10 batches
            print(f"Embedded {i + BATCH_SIZE}/{len(nodes)} nodes...")

    # Token counting (optional - can remove for speed)
    tokenizer = AutoTokenizer.from_pretrained(HF_EMBED_MODEL)
    total_tokens = sum(len(tokenizer.encode(node.text, add_special_tokens=False)) for node in nodes)
    print(f"Total Tokens: {total_tokens}, Nodes: {len(nodes)}")

    # vector store (pgvector)
    # pg_store = get_pg_store()
    # storage_context = StorageContext.from_defaults(vector_store=pg_store)
    
    #Qdrant store
    qdrant_store = get_qdrant_store()
    storage_context = StorageContext.from_defaults(vector_store=qdrant_store)


    # Use nodes with pre-computed embeddings
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    return {
        "status": "success",
        "chunks": len(nodes),
        "total_tokens": total_tokens
    }
