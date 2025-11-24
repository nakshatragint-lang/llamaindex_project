import os
import shutil
from pathlib import Path

def extract_relevant_files(repo_path: str, workspace: str) -> None:
    """
    We keep only:
      - *.py
      - *.md / *.txt / *.rst (docs)
    """
    # allowed_ext = {".py", ".md", ".txt", ".rst"}
    allowed_ext = {'.py'}

    for root, dirs, files in os.walk(repo_path):
        if ".git" in root:
            continue
        rel = os.path.relpath(root, repo_path)
        target_dir = Path(workspace) / rel
        target_dir.mkdir(parents=True, exist_ok=True)

        for f in files:
            ext = Path(f).suffix
            if ext in allowed_ext:
                shutil.copy2(Path(root) / f, target_dir / f)
