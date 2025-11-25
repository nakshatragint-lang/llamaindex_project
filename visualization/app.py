import psycopg2
import numpy as np
from sklearn.decomposition import PCA
import umap
import matplotlib.pyplot as plt
import json


# -----------------------------------------
# 1. Fetch vectors from pgvector table
# -----------------------------------------
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
        # Parse the embedding - it might be a string representation of an array
        if isinstance(emb, str):
            emb = json.loads(emb)
        vectors.append(np.array(emb, dtype=float))

    cur.close()
    conn.close()
    
    return node_ids, np.vstack(vectors)


# -----------------------------------------
# 2. Dimensionality reduction (PCA → UMAP)
# -----------------------------------------
def reduce_dimensions(vectors):
    pca = PCA(n_components=50)
    x_pca = pca.fit_transform(vectors)

    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=25,
        min_dist=0.1,
        metric="cosine",
        random_state=42
    )

    x_umap = reducer.fit_transform(x_pca)
    return x_umap


# -----------------------------------------
# 3. Plot the embedding points
# -----------------------------------------
def plot_points(points):
    plt.figure(figsize=(12, 8))
    plt.scatter(points[:, 0], points[:, 1], s=6, alpha=0.6)
    plt.title("Embedding Visualization (UMAP)")
    plt.xlabel("UMAP-1")
    plt.ylabel("UMAP-2")
    plt.show()


# -----------------------------------------
# 4. Main pipeline
# -----------------------------------------
if __name__ == "__main__":
    node_ids, vectors = fetch_vectors()
    print(f"Loaded {len(vectors)} vectors")

    points = reduce_dimensions(vectors)
    plot_points(points)
