from llama_index.vector_stores.postgres import PGVectorStore
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from config import SERVER_IP, QDRANT_PORT

def get_pg_store():
    return PGVectorStore.from_params(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="llama_db",
        table_name="repo_chunks",
        schema_name="public",
        embed_dim=1024,
        hybrid_search=False
    )

def get_qdrant_store():
    client = QdrantClient(host=SERVER_IP, port=QDRANT_PORT)
    return QdrantVectorStore(client=client, collection_name="repo_chunks", prefer_grpc=False)
