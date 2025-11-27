import xml.etree.ElementTree as ET
from pathlib import Path
from llama_index.core import Document
import logging

logger = logging.getLogger(__name__)

def chunk_xml(file_path: Path):
    nodes = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for elem in root:
            text = ET.tostring(elem, encoding="unicode")
            metadata = {"source": str(file_path), "file_type": "xml", "element_tag": elem.tag}
            nodes.append(Document(text=text, metadata=metadata))
    except Exception as e:
        logger.warning(f"Error parsing XML {file_path}: {e}")
    return nodes
