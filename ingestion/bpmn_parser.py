# import os
# from pathlib import Path
# import xml.etree.ElementTree as ET
# from collections import defaultdict, deque
# from llama_index.core import Document
# import logging

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

# # ------------------------------
# # Global BPMN Graph
# # ------------------------------

# class BPMNNode:
#     def __init__(self, node_id, text, node_type, file_path):
#         self.id = node_id
#         self.text = text
#         self.type = node_type
#         self.file_path = file_path
#         self.next_nodes = []  # IDs of connected nodes

# class BPMNGraph:
#     def __init__(self):
#         self.nodes = {}           # node_id -> BPMNNode
#         self.call_mappings = {}   # node_id -> called process_id (for subprocesses)

#     def add_node(self, node: BPMNNode):
#         self.nodes[node.id] = node

#     def add_edge(self, from_id, to_id):
#         if from_id in self.nodes:
#             self.nodes[from_id].next_nodes.append(to_id)

#     def add_call_mapping(self, node_id, called_process_id):
#         self.call_mappings[node_id] = called_process_id

# # ------------------------------
# # Parse BPMN files into nodes
# # ------------------------------

# def parse_bpmn_file(file_path: Path, graph: BPMNGraph):
#     """Parse a single BPMN file and populate the graph"""
#     try:
#         tree = ET.parse(file_path)
#         root = tree.getroot()
#         ns = {'bpmn': root.tag.split('}')[0].strip('{')}  # get namespace

#         # Map task/event/gateway ID -> BPMNNode
#         for elem in root.iter():
#             tag = elem.tag.lower()
#             node_id = elem.attrib.get('id')
#             if not node_id:
#                 continue

#             if tag.endswith(("task", "startevent", "endevent", "exclusivegateway", "subprocess")):
#                 text = ET.tostring(elem, encoding="unicode")
#                 node = BPMNNode(node_id, text, tag, str(file_path))
#                 graph.add_node(node)

#                 # Track subprocess calls
#                 if tag.endswith("subprocess"):
#                     called_process = elem.attrib.get("calledElement")
#                     if called_process:
#                         graph.add_call_mapping(node_id, called_process)

#         # Map sequenceFlows
#         for flow in root.findall(".//bpmn:sequenceFlow", ns):
#             source = flow.attrib.get("sourceRef")
#             target = flow.attrib.get("targetRef")
#             if source and target:
#                 graph.add_edge(source, target)

#     except Exception as e:
#         logger.warning(f"Error parsing BPMN file {file_path}: {e}")

# # ------------------------------
# # Generate semantic chunks
# # ------------------------------

# def generate_chunks_from_graph(graph: BPMNGraph):
#     """
#     Traverse BPMN graph and generate semantic chunks.
#     Each chunk contains a linear flow of connected nodes, including cross-file calls.
#     """
#     visited = set()
#     chunks = []

#     for node_id, node in graph.nodes.items():
#         if node_id in visited:
#             continue

#         chunk_texts = []
#         chunk_metadata = {"sources": set(), "node_ids": [], "types": [], "called_processes": []}
#         queue = deque([node_id])

#         while queue:
#             current_id = queue.popleft()
#             if current_id in visited:
#                 continue
#             visited.add(current_id)

#             current_node = graph.nodes[current_id]
#             chunk_texts.append(current_node.text)
#             chunk_metadata["sources"].add(current_node.file_path)
#             chunk_metadata["node_ids"].append(current_node.id)
#             chunk_metadata["types"].append(current_node.type)

#             # Include called subprocess info
#             if current_id in graph.call_mappings:
#                 chunk_metadata["called_processes"].append(graph.call_mappings[current_id])

#             # Add connected nodes
#             for next_id in current_node.next_nodes:
#                 if next_id not in visited:
#                     queue.append(next_id)

#         chunk_metadata["sources"] = list(chunk_metadata["sources"])
#         chunk_text = "\n".join(chunk_texts)
#         chunks.append(Document(text=chunk_text, metadata=chunk_metadata))

#     logger.info(f"Generated {len(chunks)} semantic chunks from BPMN graph")
#     return chunks

# # ------------------------------
# # High-level interface
# # ------------------------------

# def semantic_chunk_bpmn_workspace(workspace: str):
#     """Parse all BPMN files in a workspace and produce semantic chunks"""
#     graph = BPMNGraph()

#     bpmn_files = list(Path(workspace).rglob("*.bpmn"))
#     logger.info(f"Found {len(bpmn_files)} BPMN files in workspace")

#     for file_path in bpmn_files:
#         parse_bpmn_file(file_path, graph)

#     chunks = generate_chunks_from_graph(graph)
#     return chunks

import xml.etree.ElementTree as ET
from pathlib import Path
from collections import deque
from llama_index.core import Document
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class BPMNNode:
    def __init__(self, node_id, text, node_type, file_path):
        self.id = node_id
        self.text = text
        self.type = node_type
        self.file_path = file_path
        self.next_nodes = []

class BPMNGraph:
    def __init__(self):
        self.nodes = {}
        self.call_mappings = {}

    def add_node(self, node: BPMNNode):
        self.nodes[node.id] = node

    def add_edge(self, from_id, to_id):
        if from_id in self.nodes:
            self.nodes[from_id].next_nodes.append(to_id)

    def add_call_mapping(self, node_id, called_process_id):
        self.call_mappings[node_id] = called_process_id

def parse_bpmn_file(file_path: Path, graph: BPMNGraph):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'bpmn': root.tag.split('}')[0].strip('{')}

        for elem in root.iter():
            tag = elem.tag.lower()
            node_id = elem.attrib.get('id')
            if not node_id:
                continue
            if tag.endswith(("task", "startevent", "endevent", "exclusivegateway", "subprocess")):
                text = ET.tostring(elem, encoding="unicode")
                node = BPMNNode(node_id, text, tag, str(file_path))
                graph.add_node(node)
                if tag.endswith("subprocess"):
                    called_process = elem.attrib.get("calledElement")
                    if called_process:
                        graph.add_call_mapping(node_id, called_process)

        for flow in root.findall(".//bpmn:sequenceFlow", ns):
            source = flow.attrib.get("sourceRef")
            target = flow.attrib.get("targetRef")
            if source and target:
                graph.add_edge(source, target)
    except Exception as e:
        logger.warning(f"Error parsing BPMN file {file_path}: {e}")

def generate_bpmn_chunks(graph):
    """
    Traverse BPMN graph and generate semantic chunks.
    Handles missing nodes referenced in sequenceFlows gracefully.
    """
    visited = set()
    chunks = []

    for node_id, node in graph.nodes.items():
        if node_id in visited:
            continue

        chunk_texts = []
        chunk_metadata = {"sources": set(), "node_ids": [], "types": [], "called_processes": []}
        queue = deque([node_id])

        while queue:
            current_id = queue.popleft()
            if current_id in visited:
                continue

            current_node = graph.nodes.get(current_id)
            if not current_node:
                logger.warning(f"Referenced node {current_id} not found in graph.nodes. Skipping.")
                continue

            visited.add(current_id)
            chunk_texts.append(current_node.text)
            chunk_metadata["sources"].add(current_node.file_path)
            chunk_metadata["node_ids"].append(current_node.id)
            chunk_metadata["types"].append(current_node.type)

            # Include called subprocess info
            if current_id in graph.call_mappings:
                chunk_metadata["called_processes"].append(graph.call_mappings[current_id])

            # Enqueue next nodes if they exist
            for next_id in current_node.next_nodes:
                if next_id not in visited:
                    if next_id in graph.nodes:
                        queue.append(next_id)
                    else:
                        logger.warning(f"Node {next_id} referenced by {current_id} not found in graph.nodes")

        if chunk_texts:
            chunk_metadata["sources"] = list(chunk_metadata["sources"])
            chunk_text = "\n".join(chunk_texts)
            chunks.append(Document(text=chunk_text, metadata=chunk_metadata))

    logger.info(f"Generated {len(chunks)} semantic chunks from BPMN graph")
    return chunks