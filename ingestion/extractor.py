import os
import shutil
from pathlib import Path

def extract_relevant_files(repo_path: str, workspace: str) -> None:
    """
    Extract only relevant Python files, skipping large/binary files
    """
    allowed_ext = {'.py'}
    
    # Directories to skip
    skip_dirs = {
        '.git', '__pycache__', 'node_modules', 'venv', 'env', 
        '.venv', 'dist', 'build', '.pytest_cache', '.tox',
        'db_data', 'venv_old', 'tests'  # Skip your test artifacts
    }
    
    # Maximum file size (1MB)
    MAX_FILE_SIZE = 1_000_000
    
    file_count = 0
    
    for root, dirs, files in os.walk(repo_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        if any(skip in root for skip in skip_dirs):
            continue
            
        rel = os.path.relpath(root, repo_path)
        target_dir = Path(workspace) / rel
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for f in files:
            src_path = Path(root) / f
            
            # Check file size
            try:
                if src_path.stat().st_size > MAX_FILE_SIZE:
                    print(f"Skipping large file: {src_path}")
                    continue
            except:
                continue
            
            ext = Path(f).suffix
            if ext in allowed_ext:
                shutil.copy2(src_path, target_dir / f)
                file_count += 1
    
    print(f"Extracted {file_count} files to workspace")
