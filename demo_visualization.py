"""
Demo script to visualize embeddings from the vector database.
"""

from visualization import EmbeddingVisualizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Demonstrate embedding visualization capabilities.
    """
    # Initialize visualizer
    visualizer = EmbeddingVisualizer()
    
    # Load embeddings from TSV file
    logger.info("Loading embeddings from file...")
    visualizer.load_embeddings_from_file('embeddings.tsv')
    
    # Check the data
    print(f"\nDataFrame shape: {visualizer.embeddings_df.shape}")
    print(f"Columns: {visualizer.embeddings_df.columns.tolist()}")
    print(f"\nFirst few rows:")
    print(visualizer.embeddings_df.head())
    
    # Reduce dimensions using PCA
    logger.info("\nReducing dimensions with PCA (2D)...")
    visualizer.reduce_dimensions(method='pca', n_components=2)
    
    # Create 2D static plot
    logger.info("Creating 2D static plot...")
    visualizer.plot_2d_static(
        title="Embeddings Visualization (PCA 2D)",
        save_path="embeddings_2d_static.png"
    )
    
    # Create 2D interactive plot
    logger.info("Creating 2D interactive plot...")
    visualizer.plot_2d_interactive(
        title="Interactive Embeddings Visualization (PCA 2D)",
        save_path="embeddings_2d_interactive.html"
    )
    
    # Create 3D visualization only if we have enough samples
    num_samples = len(visualizer.embeddings_df)
    if num_samples >= 3:
        # Reduce to 3D for 3D visualization
        logger.info("\nReducing dimensions with PCA (3D)...")
        visualizer.reduce_dimensions(method='pca', n_components=3)
        
        # Create 3D interactive plot
        logger.info("Creating 3D interactive plot...")
        visualizer.plot_3d_interactive(
            title="Interactive 3D Embeddings Visualization (PCA)",
            save_path="embeddings_3d_interactive.html"
        )
    else:
        logger.info(f"\nSkipping 3D visualization (need at least 3 samples, have {num_samples})")
    
    # Create similarity heatmap
    logger.info("\nCreating similarity heatmap...")
    sample_size = min(50, num_samples)  # Use actual number if less than 50
    visualizer.plot_heatmap(
        sample_size=sample_size,
        title="Embedding Similarity Matrix",
        save_path="embeddings_heatmap.png"
    )
    
    logger.info("\n✅ Visualization complete!")
    logger.info("Generated files:")
    logger.info("  - embeddings_2d_static.png (static 2D plot)")
    logger.info("  - embeddings_2d_interactive.html (interactive 2D plot)")
    if num_samples >= 3:
        logger.info("  - embeddings_3d_interactive.html (interactive 3D plot)")
    logger.info("  - embeddings_heatmap.png (similarity heatmap)")


if __name__ == "__main__":
    main()
