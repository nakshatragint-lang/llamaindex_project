import tempfile
from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext, Settings

from .clone import clone_repo
from .extractor import extract_relevant_files
from .chunker import chunk_repo_files
from .embedder import get_embedder
from .vector_store import get_pg_store


def ingest_repo_service(repo_url: str):
    repo_path = clone_repo(repo_url)

    workspace = tempfile.mkdtemp()
    extract_relevant_files(repo_path, workspace)

    # chunking
    nodes = chunk_repo_files(workspace)

    # embedding
    embedder = get_embedder()
    Settings.embed_model = embedder

    # vector store (pgvector)
    pg_store = get_pg_store()

    # build index INSIDE the vector store
    storage_context = StorageContext.from_defaults(vector_store=pg_store)

    index = VectorStoreIndex.from_documents(
        nodes,
        storage_context=storage_context
    )

    return {
        "status": "success",
        "chunks": len(nodes)
    }
