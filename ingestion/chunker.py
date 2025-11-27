# import os
# from pathlib import Path
# from llama_index.core import Document
# from llama_index.core.node_parser import CodeSplitter, SimpleNodeParser
# from concurrent.futures import ProcessPoolExecutor, as_completed
# import multiprocessing
# import logging

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

# # Mapping file extensions to code languages or type
# EXT_LANGUAGE_MAP = {
#     ".py": "python",
#     ".java": "java",
#     ".bpmn": None,  # treat as text
#     ".xml": None    # treat as text
# }

# def process_single_file(file_path: Path):
#     """
#     Process a single file and return its nodes.
#     Uses CodeSplitter for code, SimpleNodeParser for text files.
#     """
#     try:
#         text = file_path.read_text(errors="ignore")
#         ext = file_path.suffix.lower()

#         # Decide splitter
#         if EXT_LANGUAGE_MAP.get(ext):
#             splitter = CodeSplitter(
#                 language=EXT_LANGUAGE_MAP[ext],
#                 chunk_lines=80,
#                 chunk_lines_overlap=20,
#                 max_chars=3000
#             )
#         else:
#             splitter = SimpleNodeParser.from_defaults(
#                 chunk_size=1024,
#                 chunk_overlap=100
#             )

#         doc = Document(text=text)
#         new_nodes = splitter.get_nodes_from_documents([doc])

#         for n in new_nodes:
#             n.metadata = {"source": str(file_path), "file_type": ext[1:]}

#         return new_nodes

#     except Exception as e:
#         logger.warning(f"Error processing {file_path}: {e}")
#         return []

# def chunk_repo_files(workspace: str):
#     """
#     Chunk files in a repo workspace in parallel.
#     Returns a list of nodes.
#     """
#     files_to_process = [
#         Path(root) / f
#         for root, _, files in os.walk(workspace)
#         for f in files
#         if (Path(root) / f).is_file()
#     ]

#     nodes = []
#     max_workers = min(multiprocessing.cpu_count(), len(files_to_process))

#     logger.info(f"Processing {len(files_to_process)} files with {max_workers} workers...")

#     with ProcessPoolExecutor(max_workers=max_workers) as executor:
#         futures = {executor.submit(process_single_file, fp): fp for fp in files_to_process}

#         for i, future in enumerate(as_completed(futures), 1):
#             try:
#                 result = future.result()
#                 nodes.extend(result)
#             except Exception as e:
#                 logger.warning(f"Error in future for {futures[future]}: {e}")

#             if i % 50 == 0 or i == len(futures):
#                 logger.info(f"Processed {i}/{len(futures)} files...")

#     logger.info(f"Total nodes created: {len(nodes)}")
#     return nodes

import os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import logging

from .bpmn_parser import BPMNGraph, parse_bpmn_file, generate_bpmn_chunks
from .xml_parser import chunk_xml
from .code_parser import process_code_file
from llama_index.core import Document

logger = logging.getLogger(__name__)


# --------------------------------------------------------
# WORKER MUST BE TOP-LEVEL (NOT INSIDE ANY FUNCTION)
# --------------------------------------------------------
def chunk_file_worker(fp: str):
    """Multiprocessing-safe worker for non-BPMN files."""
    fp = Path(fp)
    ext = fp.suffix.lower()

    try:
        if ext in [".py", ".java"]:
            return process_code_file(fp)
        elif ext == ".xml":
            return chunk_xml(fp)
        else:
            return []
    except Exception as e:
        return []


# --------------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------------
def chunk_repo_files(workspace: str):
    workspace = Path(workspace)

    # ---- 1. PROCESS BPMN ----
    graph = BPMNGraph()
    bpmn_files = list(workspace.rglob("*.bpmn"))

    logger.info(f"Found {len(bpmn_files)} BPMN files")

    for file_path in bpmn_files:
        parse_bpmn_file(file_path, graph)

    bpmn_chunks = generate_bpmn_chunks(graph)

    # ---- 2. COLLECT ALL OTHER FILES ----
    files_to_process = [
        Path(root) / f
        for root, _, files in os.walk(workspace)
        for f in files
        if (Path(root) / f).is_file() and not f.lower().endswith(".bpmn")
    ]

    logger.info(f"Found {len(files_to_process)} non-BPMN files")

    # ---- 3. PARALLEL PROCESS NON-BPMN ----
    max_workers = min(multiprocessing.cpu_count(), len(files_to_process))
    nodes = []

    if max_workers > 0:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(chunk_file_worker, str(fp)): fp
                for fp in files_to_process
            }

            for i, future in enumerate(as_completed(futures), 1):
                try:
                    results = future.result()
                    nodes.extend(results)
                except Exception as e:
                    logger.warning(f"Error processing {futures[future]}: {e}")

                if i % 50 == 0 or i == len(futures):
                    logger.info(f"Processed {i}/{len(futures)} files...")

    # ---- 4. MERGE RESULTS ----
    total_nodes = bpmn_chunks + nodes
    logger.info(f"Total chunks generated: {len(total_nodes)}")

    return total_nodes
