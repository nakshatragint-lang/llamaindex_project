# from pathlib import Path
# from llama_index.core import Document
# from llama_index.core.node_parser import CodeSplitter, SimpleNodeParser

# def split_files(directory: str):
#     docs = []

#     for path in Path(directory).rglob("*"):
#         if not path.is_file():
#             continue

#         text = path.read_text(errors="ignore")

#         if path.suffix == ".py":
#             splitter = CodeSplitter(
#                 language="python",
#                 chunk_lines=40,
#                 chunk_lines_overlap=10,
#                 max_chars=1500
#             )
#             nodes = splitter.get_nodes_from_documents([Document(text)])
#         else:
#             splitter = SimpleNodeParser.from_defaults(
#                 chunk_size=1024, chunk_overlap=100
#             )
#             nodes = splitter.get_nodes_from_documents([Document(text)])

#         for n in nodes:
#             n.metadata = {"source": str(path)}
#             docs.append(n)

#     return docs

import os
from pathlib import Path
from llama_index.core import Document
from llama_index.core.node_parser import CodeSplitter, SimpleNodeParser

def chunk_repo_files(workspace: str):
    nodes = []

    for root, dirs, files in os.walk(workspace):
        for f in files:
            file_path = Path(root, f)
            if not file_path.is_file():
                continue

            text = file_path.read_text(errors="ignore")

            # Use built-in CodeSplitter for Python code
            if f.endswith(".py"):
                splitter = CodeSplitter(
                    language="python",
                    chunk_lines=80,
                    chunk_lines_overlap=20, 
                    max_chars=3000
                )
                doc = Document(text=text)
                new_nodes = splitter.get_nodes_from_documents([doc])

            # Use simple text splitter for docs
            else:
                parser = SimpleNodeParser.from_defaults(
                    chunk_size=1024,
                    chunk_overlap=100
                )
                doc = Document(text=text)
                new_nodes = parser.get_nodes_from_documents([doc])

            # Add metadata
            for n in new_nodes:
                n.metadata = {"source": str(file_path)}

            nodes.extend(new_nodes)
    return nodes
