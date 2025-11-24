from llama_index.core import VectorStoreIndex
from ingestion.vector_store import get_pg_store
from ingestion.embedder import get_embedder


def retrieve_chunks( query: str):
    pg_store = get_pg_store()

    # use the SAME embedder you used during ingestion
    embedder = get_embedder()

    index = VectorStoreIndex.from_vector_store(
        vector_store=pg_store,
        embed_model=embedder
    )

    retriever = index.as_retriever(similarity_top_k=6)
    results = retriever.retrieve(query)
    if not results:
        return ""
    return "\n\n".join([r.get_text() for r in results])
