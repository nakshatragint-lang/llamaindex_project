import os
from pathlib import Path
from llama_index.core import Document
from llama_index.core.node_parser import CodeSplitter, SimpleNodeParser
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing


def process_single_file(file_info):
    """Process a single file and return its nodes"""
    file_path, root = file_info
    
    try:
        text = file_path.read_text(errors="ignore")
        
        if file_path.suffix == ".py":
            splitter = CodeSplitter(
                language="python",
                chunk_lines=80,
                chunk_lines_overlap=20, 
                max_chars=3000
            )
        else:
            splitter = SimpleNodeParser.from_defaults(
                chunk_size=1024,
                chunk_overlap=100
            )
        
        doc = Document(text=text)
        new_nodes = splitter.get_nodes_from_documents([doc])
        
        for n in new_nodes:
            n.metadata = {"source": str(file_path)}
        
        return new_nodes
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []


def chunk_repo_files(workspace: str):
    """Chunk files in parallel for faster processing"""
    files_to_process = []
    
    for root, dirs, files in os.walk(workspace):
        for f in files:
            file_path = Path(root, f)
            if file_path.is_file():
                files_to_process.append((file_path, root))
    
    nodes = []
    max_workers = min(multiprocessing.cpu_count(), len(files_to_process))
    
    print(f"Processing {len(files_to_process)} files with {max_workers} workers...")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_file, fp): fp for fp in files_to_process}
        
        for future in as_completed(futures):
            try:
                result = future.result()
                nodes.extend(result)
            except Exception as e:
                print(f"Error in future: {e}")
    
    return nodes
