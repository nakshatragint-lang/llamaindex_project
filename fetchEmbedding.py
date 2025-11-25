import psycopg2
import numpy as np

def fetch_vectors():
    conn = psycopg2.connect(
        dbname="llama_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432,
    )
    
    cur = conn.cursor()
    cur.execute("SELECT node_id, embedding FROM data_fast_api WHERE embedding IS NOT NULL")
    rows = cur.fetchall()

    node_ids = []
    vectors = []

    for nid, emb in rows:
        node_ids.append(nid)
        vectors.append(np.array(emb, dtype=float))  # convert pgvector → numpy

    return node_ids, np.vstack(vectors)
