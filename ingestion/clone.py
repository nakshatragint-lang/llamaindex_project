import hashlib
from pathlib import Path
import shutil
from git import Repo
from config import CLONE_BASE


def clone_repo(url: str) -> str:
    repo_id = hashlib.sha1(url.encode()).hexdigest()[:10]
    path = Path(CLONE_BASE) / repo_id

    if path.exists():
        try:
            repo = Repo(str(path))
            repo.remotes.origin.pull()
            return str(path)
        except:
            shutil.rmtree(path)

    Repo.clone_from(url, str(path))
    return str(path)
