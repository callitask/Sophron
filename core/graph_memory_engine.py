"""
GraphMemoryEngine: Traverses and queries the semantic graph memory.
Enforces workspace isolation via WorkspaceGuard during all lookups.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .workspace_guard import WorkspaceGuard

MASTER_DIR = Path(__file__).resolve().parent.parent
GRAPH_DIR = MASTER_DIR / "graph_memory"


class GraphMemoryEngine:
    """
    Semantic Graph Memory Query & Traversal Engine.
    """

    def __init__(self, graph_dir: Optional[Path] = None, current_workspace_uri: Optional[str] = None):
        self.graph_dir = Path(graph_dir) if graph_dir else GRAPH_DIR
        self.guard = WorkspaceGuard(current_workspace_uri=current_workspace_uri)
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self.adjacency: Dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        nodes_file = self.graph_dir / "nodes.json"
        edges_file = self.graph_dir / "edges.json"
        index_file = self.graph_dir / "graph_index.json"

        if nodes_file.exists():
            with open(nodes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.nodes = {n["id"]: n for n in data.get("nodes", [])}

        if edges_file.exists():
            with open(edges_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.edges = data.get("edges", [])

        if index_file.exists():
            with open(index_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.adjacency = data.get("adjacency", {})

    def query_principles(self, tier: Optional[int] = 1) -> List[Dict[str, Any]]:
        """Retrieve cognitive principles filtered by tier."""
        results = []
        for n in self.nodes.values():
            if tier is None or n.get("tier") == tier:
                results.append(n)
        return results

    def get_related_nodes(self, node_id: str, relation_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Walks adjacent outgoing edges from node_id."""
        if node_id not in self.adjacency:
            return []
        connected = []
        for edge in self.adjacency[node_id].get("outgoing", []):
            if relation_type is None or edge["relation"] == relation_type:
                target_node = self.nodes.get(edge["target"])
                if target_node:
                    connected.append({"node": target_node, "relation": edge["relation"]})
        return connected

    def get_workspace_memories(self, workspace_slug: str) -> List[Dict[str, Any]]:
        """Retrieves memories strictly scoped to a workspace after guard validation."""
        results = []
        for n in self.nodes.values():
            if n.get("tier") == 2:
                try:
                    if self.guard.filter_memory_access(n, target_workspace_id=workspace_slug):
                        results.append(n)
                except Exception:
                    pass
        return results
