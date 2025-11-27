from llama_index.core import VectorStoreIndex
from ingestion.vector_store import get_pg_store
from ingestion.embedder import get_embedder


def retrieve_chunks(query: str):
    pg_store = get_pg_store()

    # use the SAME embedder you used during ingestion
    embedder = get_embedder()

    index = VectorStoreIndex.from_vector_store(
        vector_store=pg_store,
        embed_model=embedder
    )

    retriever = index.as_retriever(similarity_top_k=5)
    results = retriever.retrieve(query)
    
    if not results:
        return ""
    
    # Log detailed information about retrieved chunks
    print("\n" + "="*80)
    print(f"QUERY: {query}")
    print("="*80)
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Chunk {i} (Score: {result.score:.4f}) ---")
        print(f"Source: {result.metadata.get('source', 'Unknown')}")
        print(f"Node ID: {result.node_id}")
        print(f"Text Preview: {result.text[:200]}...")
        print("-" * 80)
    
    return "\n\n".join([r.get_text() for r in results])
