"""
Visualization module for embedding data from vector database.
Provides functionality to extract, process, and visualize embeddings.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from typing import List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingVisualizer:
    """
    Class to handle visualization of embedding data from vector database.
    """
    
    def __init__(self, vector_store=None):
        """
        Initialize the visualizer with optional vector store connection.
        
        Args:
            vector_store: Vector store instance to query embeddings from
        """
        self.vector_store = vector_store
        self.embeddings_df = None
        self.reduced_embeddings = None
    
    def load_embeddings_from_db(self) -> pd.DataFrame:
        """
        Load embeddings from the vector database.
        
        Returns:
            DataFrame containing embeddings and metadata
        """
        # TODO: Implement database query logic
        logger.info("Loading embeddings from vector database...")
        pass
    
    def load_embeddings_from_file(self, filepath: str) -> pd.DataFrame:
        """
        Load embeddings from a file (CSV/TSV).
        
        Args:
            filepath: Path to the embeddings file
            
        Returns:
            DataFrame containing embeddings and metadata
        """
        logger.info(f"Loading embeddings from file: {filepath}")
        
        if filepath.endswith('.tsv'):
            df = pd.read_csv(filepath, sep='\t', header=None)
        elif filepath.endswith('.csv'):
            df = pd.read_csv(filepath, header=None)
        else:
            raise ValueError("Unsupported file format. Use CSV or TSV.")
        
        # Parse the embedding strings into arrays
        import json
        embeddings_list = []
        for idx, row in df.iterrows():
            # Get the first column which contains the embedding string
            embedding_str = row[0]
            # Parse the string as a JSON array
            embedding = json.loads(embedding_str)
            embeddings_list.append(embedding)
        
        # Convert to DataFrame with separate columns for each dimension
        self.embeddings_df = pd.DataFrame(embeddings_list)
        
        logger.info(f"Loaded {len(self.embeddings_df)} embeddings with {self.embeddings_df.shape[1]} dimensions")
        return self.embeddings_df
    
    def reduce_dimensions(self, method: str = 'pca', n_components: int = 2) -> np.ndarray:
        """
        Reduce dimensionality of embeddings for visualization.
        
        Args:
            method: 'pca' or 'tsne'
            n_components: Number of dimensions to reduce to (2 or 3)
            
        Returns:
            Reduced embeddings array
        """
        if self.embeddings_df is None:
            raise ValueError("No embeddings loaded. Call load_embeddings first.")
        
        # Extract embedding columns (assuming they're numeric)
        embedding_cols = self.embeddings_df.select_dtypes(include=[np.number]).columns
        embeddings = self.embeddings_df[embedding_cols].values
        
        logger.info(f"Reducing dimensions using {method}...")
        
        if method.lower() == 'pca':
            reducer = PCA(n_components=n_components)
            self.reduced_embeddings = reducer.fit_transform(embeddings)
            logger.info(f"Explained variance: {reducer.explained_variance_ratio_}")
        elif method.lower() == 'tsne':
            reducer = TSNE(n_components=n_components, random_state=42)
            self.reduced_embeddings = reducer.fit_transform(embeddings)
        else:
            raise ValueError("Method must be 'pca' or 'tsne'")
        
        return self.reduced_embeddings
    
    def plot_2d_static(self, labels: Optional[List] = None, title: str = "Embedding Visualization",
                      save_path: Optional[str] = None):
        """
        Create static 2D scatter plot using Matplotlib.
        
        Args:
            labels: Optional labels for coloring points
            title: Plot title
            save_path: Optional path to save the figure (e.g., 'plot.png')
        """
        if self.reduced_embeddings is None or self.reduced_embeddings.shape[1] != 2:
            raise ValueError("Run reduce_dimensions with n_components=2 first")
        
        plt.figure(figsize=(12, 8))
        
        if labels is not None:
            scatter = plt.scatter(
                self.reduced_embeddings[:, 0],
                self.reduced_embeddings[:, 1],
                c=labels,
                cmap='viridis',
                alpha=0.6,
                edgecolors='w',
                linewidth=0.5
            )
            plt.colorbar(scatter)
        else:
            plt.scatter(
                self.reduced_embeddings[:, 0],
                self.reduced_embeddings[:, 1],
                alpha=0.6,
                edgecolors='w',
                linewidth=0.5
            )
        
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.title(title)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        
        plt.show()
    
    def plot_2d_interactive(self, labels: Optional[List] = None, 
                           hover_data: Optional[pd.DataFrame] = None,
                           title: str = "Interactive Embedding Visualization",
                           save_path: Optional[str] = None):
        """
        Create interactive 2D scatter plot using Plotly.
        
        Args:
            labels: Optional labels for coloring points
            hover_data: Additional data to show on hover
            title: Plot title
            save_path: Optional path to save as HTML (e.g., 'plot.html')
        """
        if self.reduced_embeddings is None or self.reduced_embeddings.shape[1] != 2:
            raise ValueError("Run reduce_dimensions with n_components=2 first")
        
        df_plot = pd.DataFrame({
            'x': self.reduced_embeddings[:, 0],
            'y': self.reduced_embeddings[:, 1]
        })
        
        if labels is not None:
            df_plot['label'] = labels
            color_col = 'label'
        else:
            color_col = None
        
        if hover_data is not None:
            df_plot = pd.concat([df_plot, hover_data], axis=1)
        
        fig = px.scatter(
            df_plot,
            x='x',
            y='y',
            color=color_col,
            hover_data=hover_data.columns.tolist() if hover_data is not None else None,
            title=title,
            labels={'x': 'Component 1', 'y': 'Component 2'}
        )
        
        fig.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0.5, color='white')))
        fig.update_layout(height=700, width=1000)
        
        if save_path:
            fig.write_html(save_path)
            logger.info(f"Interactive plot saved to {save_path}")
        
        fig.show()
    
    def plot_3d_interactive(self, labels: Optional[List] = None,
                           hover_data: Optional[pd.DataFrame] = None,
                           title: str = "3D Embedding Visualization",
                           save_path: Optional[str] = None):
        """
        Create interactive 3D scatter plot using Plotly.
        
        Args:
            labels: Optional labels for coloring points
            hover_data: Additional data to show on hover
            title: Plot title
            save_path: Optional path to save as HTML (e.g., 'plot_3d.html')
        """
        if self.reduced_embeddings is None or self.reduced_embeddings.shape[1] != 3:
            raise ValueError("Run reduce_dimensions with n_components=3 first")
        
        df_plot = pd.DataFrame({
            'x': self.reduced_embeddings[:, 0],
            'y': self.reduced_embeddings[:, 1],
            'z': self.reduced_embeddings[:, 2]
        })
        
        if labels is not None:
            df_plot['label'] = labels
            color_col = 'label'
        else:
            color_col = None
        
        if hover_data is not None:
            df_plot = pd.concat([df_plot, hover_data], axis=1)
        
        fig = px.scatter_3d(
            df_plot,
            x='x',
            y='y',
            z='z',
            color=color_col,
            hover_data=hover_data.columns.tolist() if hover_data is not None else None,
            title=title,
            labels={'x': 'Component 1', 'y': 'Component 2', 'z': 'Component 3'}
        )
        
        fig.update_traces(marker=dict(size=5, opacity=0.7, line=dict(width=0.5, color='white')))
        fig.update_layout(height=700, width=1000)
        
        if save_path:
            fig.write_html(save_path)
            logger.info(f"3D interactive plot saved to {save_path}")
        
        fig.show()
    
    def plot_heatmap(self, sample_size: int = 50, title: str = "Embedding Similarity Heatmap",
                    save_path: Optional[str] = None):
        """
        Create heatmap showing similarity between embeddings.
        
        Args:
            sample_size: Number of embeddings to include (for performance)
            title: Plot title
            save_path: Optional path to save the figure (e.g., 'heatmap.png')
        """
        if self.embeddings_df is None:
            raise ValueError("No embeddings loaded. Call load_embeddings first.")
        
        embedding_cols = self.embeddings_df.select_dtypes(include=[np.number]).columns
        embeddings = self.embeddings_df[embedding_cols].values[:sample_size]
        
        # Compute cosine similarity
        from sklearn.metrics.pairwise import cosine_similarity
        similarity_matrix = cosine_similarity(embeddings)
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(similarity_matrix, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title(title)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Heatmap saved to {save_path}")
        
        plt.show()


def main():
    """
    Example usage of the EmbeddingVisualizer.
    """
    # Initialize visualizer
    visualizer = EmbeddingVisualizer()
    
    # Load embeddings from file
    # visualizer.load_embeddings_from_file('embeddings.tsv')
    
    # Reduce dimensions
    # visualizer.reduce_dimensions(method='pca', n_components=2)
    
    # Create visualizations
    # visualizer.plot_2d_static()
    # visualizer.plot_2d_interactive()
    # visualizer.plot_3d_interactive()
    # visualizer.plot_heatmap()
    
    logger.info("Visualization module ready")


if __name__ == "__main__":
    main()
