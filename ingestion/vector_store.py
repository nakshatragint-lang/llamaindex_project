from llama_index.vector_stores.postgres import PGVectorStore

def get_pg_store():
    return PGVectorStore.from_params(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="llama_db",
        table_name="public_repo_chunks",
        schema_name="public",
        embed_dim=384,    # Embedding dimension for the model being used
        hybrid_search=False
    )
