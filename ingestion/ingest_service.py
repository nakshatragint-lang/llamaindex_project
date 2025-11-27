import tempfile
import shutil
from pathlib import Path
import logging
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from transformers import AutoTokenizer
from .clone import clone_repo
from .extractor import extract_relevant_files
from .chunker import chunk_repo_files
from .embedder import get_embedder
from .vector_store import get_qdrant_store
from config import HF_EMBED_MODEL

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_repo_service(repo_url: str, count_tokens: bool = True):
    """
    Ingest a repo into Qdrant with precomputed embeddings.
    Args:
        repo_url (str): URL of the git repo
        count_tokens (bool): Whether to calculate token count (optional, slow for large repos)
    Returns:
        dict: Status info including chunks processed and total tokens
    """
    try:
        # Clone repository
        repo_path = clone_repo(repo_url)
    except Exception as e:
        logger.error(f"Failed to clone repo: {e}")
        return {"status": "error", "message": "Clone failed"}

    # Temporary workspace
    workspace = tempfile.mkdtemp()
    try:
        extract_relevant_files(repo_path, workspace)
        nodes = chunk_repo_files(workspace)
        java_nodes = [n for n in nodes if n.metadata['source'].endswith('.java')]
        bpmn_nodes = [n for n in nodes if n.metadata['source'].endswith('.bpmn')]
        xml_nodes  = [n for n in nodes if n.metadata['source'].endswith('.xml')]

        print(f"Java nodes: {len(java_nodes)}, BPMN nodes: {len(bpmn_nodes)}, XML nodes: {len(xml_nodes)}")

        if not nodes:
            logger.warning("No chunks generated from repository")
            return {"status": "warning", "chunks": 0}

        # Embedding setup
        embedder = get_embedder()
        Settings.embed_model = embedder
        BATCH_SIZE = 32

        logger.info(f"Embedding {len(nodes)} nodes in batches...")
        for i in range(0, len(nodes), BATCH_SIZE):
            batch = nodes[i:i + BATCH_SIZE]
            texts = [node.text for node in batch]
            try:
                embeddings = embedder.get_text_embedding_batch(texts)
            except Exception as e:
                logger.error(f"Embedding failed for batch {i}-{i + len(batch)}: {e}")
                continue
            for node, emb in zip(batch, embeddings):
                node.embedding = emb

            if (i + len(batch)) % 320 == 0 or (i + len(batch)) == len(nodes):
                logger.info(f"Embedded {i + len(batch)}/{len(nodes)} nodes...")

        # Token counting (optional)
        total_tokens = 0
        if count_tokens:
            tokenizer = AutoTokenizer.from_pretrained(HF_EMBED_MODEL)
            total_tokens = sum(
                len(tokenizer.encode(node.text, add_special_tokens=False)) for node in nodes
            )
            logger.info(f"Total Tokens: {total_tokens}, Nodes: {len(nodes)}")

        # Qdrant vector store
        qdrant_store = get_qdrant_store()

        # Ensure collection exists with correct dimensions
        client = qdrant_store.client
        collection_name = qdrant_store.collection_name
        vector_dim = len(nodes[0].embedding)
        if collection_name not in [c.name for c in client.get_collections().collections]:
            logger.info(f"Creating Qdrant collection '{collection_name}' with dimension {vector_dim}")
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config={"size": vector_dim, "distance": "Cosine"}
            )

        storage_context = StorageContext.from_defaults(vector_store=qdrant_store)
        index = VectorStoreIndex(nodes, storage_context=storage_context)

    finally:
        # Clean up temp workspace
        shutil.rmtree(workspace)

    return {
        "status": "success",
        "chunks": len(nodes),
        "total_tokens": total_tokens
    }
