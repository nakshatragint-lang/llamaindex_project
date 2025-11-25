import psycopg2
import numpy as np
from sklearn.decomposition import PCA
import umap
import pandas as pd
import plotly.express as px
import json


# -----------------------------------------
# 1. Fetch vectors from pgvector
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
    cur.execute("""
        SELECT node_id, text, embedding 
        FROM data_fast_api 
        WHERE embedding IS NOT NULL
    """)

    rows = cur.fetchall()

    node_ids = []
    texts = []
    vectors = []

    for nid, txt, emb in rows:
        node_ids.append(nid)
        texts.append(txt[:300] if txt else "")   # limit hover text to 300 chars for performance
        
        # Parse the embedding - it might be a string representation of an array
        if isinstance(emb, str):
            emb = json.loads(emb)
        vectors.append(np.array(emb, dtype=float))

    cur.close()
    conn.close()
    
    return node_ids, texts, np.vstack(vectors)


# -----------------------------------------
# 2. Dimensionality reduction
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
# 3. Build interactive Plotly graph
# -----------------------------------------
def build_interactive_plot(points, node_ids, texts):
    df = pd.DataFrame({
        "x": points[:, 0],
        "y": points[:, 1],
        "node_id": node_ids,
        "text": texts
    })

    fig = px.scatter(
        df,
        x="x", y="y",
        hover_data={"node_id": True, "text": True, "x": False, "y": False},
        opacity=0.7,
        title="Interactive Embedding Visualization (UMAP) - Hover to see text chunks"
    )

    fig.update_traces(
        marker=dict(size=6, line=dict(width=0.5, color='DarkSlateGrey')),
        hovertemplate="<b>Node ID:</b> %{customdata[0]}<br><b>Text:</b> %{customdata[1]}<extra></extra>"
    )
    
    fig.update_layout(
        width=1200,
        height=800,
        xaxis_title="UMAP Dimension 1",
        yaxis_title="UMAP Dimension 2",
        font=dict(size=12)
    )
    
    # Save to HTML file for easy sharing
    fig.write_html("embeddings_2d_interactive.html")
    print("✅ Saved interactive plot to: embeddings_2d_interactive.html")
    
    # Open in browser
    fig.show()


# -----------------------------------------
# 4. Main pipeline
# -----------------------------------------
if __name__ == "__main__":
    node_ids, texts, vectors = fetch_vectors()
    print(f"Loaded {len(vectors)} embeddings")

    points = reduce_dimensions(vectors)
    build_interactive_plot(points, node_ids, texts)
