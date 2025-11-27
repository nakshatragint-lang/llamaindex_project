import os
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def extract_relevant_files(repo_path: str, workspace: str, allowed_ext=None, max_file_size=1_000_000) -> None:
    """
    Extract only relevant files from a repo into a workspace.
    
    Args:
        repo_path (str): Path to the cloned repository.
        workspace (str): Path to the temporary workspace.
        allowed_ext (set, optional): File extensions to include. Defaults to {'.java', '.bpmn', '.xml'}.
        max_file_size (int, optional): Maximum file size in bytes. Defaults to 1MB.
    """
    if allowed_ext is None:
        allowed_ext = {'.java', '.bpmn', '.xml', '.py'}

    # Directories to skip
    skip_dirs = {
        '.git', '__pycache__', 'node_modules', 'venv', 'env', 
        '.venv', 'dist', 'build', '.pytest_cache', '.tox',
        'db_data', 'venv_old', 'tests'
    }

    file_count = 0

    for root, dirs, files in os.walk(repo_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        # Skip any path that contains excluded directories
        if any(skip in root for skip in skip_dirs):
            continue

        rel = os.path.relpath(root, repo_path)
        target_dir = Path(workspace) / rel
        target_dir.mkdir(parents=True, exist_ok=True)

        for f in files:
            src_path = Path(root) / f
            
            # Skip large files
            try:
                if src_path.stat().st_size > max_file_size:
                    logger.debug(f"Skipping large file: {src_path}")
                    continue
            except Exception as e:
                logger.warning(f"Could not stat file {src_path}: {e}")
                continue

            ext = src_path.suffix.lower()
            if ext in allowed_ext:
                try:
                    shutil.copy2(src_path, target_dir / f)
                    file_count += 1
                except Exception as e:
                    logger.warning(f"Failed to copy {src_path}: {e}")
                    continue

    logger.info(f"Extracted {file_count} files to workspace: {workspace}")
