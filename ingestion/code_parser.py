from pathlib import Path
from llama_index.core.node_parser import CodeSplitter
from llama_index.core import Document
import logging

logger = logging.getLogger(__name__)

EXT_LANGUAGE_MAP = {
    ".py": "python",
    ".java": "java"
}

def process_code_file(file_path: Path):
    ext = file_path.suffix.lower()
    if ext not in EXT_LANGUAGE_MAP:
        return []

    try:
        text = file_path.read_text(errors="ignore")
        splitter = CodeSplitter(
            language=EXT_LANGUAGE_MAP[ext],
            chunk_lines=80,
            chunk_lines_overlap=20,
            max_chars=3000
        )
        doc = Document(text=text)
        nodes = splitter.get_nodes_from_documents([doc])
        for n in nodes:
            n.metadata.update({"source": str(file_path), "file_type": ext[1:]})
        return nodes
    except Exception as e:
        logger.warning(f"Error processing code file {file_path}: {e}")
        return []
