"""
GenAI Platform - Knowledge Graph Manager
Entity models, relationship mapping, and graph-based operations
"""

import networkx as nx
import pickle
from typing import Dict, List, Any, Optional
from pathlib import Path
from loguru import logger


class KnowledgeGraphManager:
    """Manages knowledge graph with entity models and relationships."""
    
    def __init__(self, graph_path: Optional[str] = None):
        """Initialize knowledge graph manager."""
        if graph_path is None:
            graph_path = Path.cwd() / "data" / "knowledge_graph" / "graph.pkl"
        
        self.graph_path = Path(graph_path)
        self.graph_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.graph = nx.MultiDiGraph()
        self._load_graph()
        
        logger.info("KnowledgeGraphManager initialized")
    
    def _load_graph(self):
        """Load graph from disk."""
        if self.graph_path.exists():
            try:
                with open(self.graph_path, 'rb') as f:
                    self.graph = pickle.load(f)
                logger.info(f"Loaded graph with {self.graph.number_of_nodes()} nodes")
            except:
                self.graph = nx.MultiDiGraph()
    
    def _save_graph(self):
        """Save graph to disk."""
        try:
            with open(self.graph_path, 'wb') as f:
                pickle.dump(self.graph, f)
            logger.debug("Graph saved")
        except Exception as e:
            logger.error(f"Error saving graph: {e}")
    
    def add_entity(
        self,
        entity_id: str,
        entity_type: str,
        properties: Dict[str, Any],
        division_id: str
    ):
        """
        Add entity to knowledge graph.
        
        Args:
            entity_id: Unique entity ID
            entity_type: Type (Employee, Customer, Vendor, Product, etc.)
            properties: Entity properties
            division_id: Division for isolation
        """
        self.graph.add_node(
            entity_id,
            entity_type=entity_type,
            division_id=division_id,
            **properties
        )
        self._save_graph()
        logger.debug(f"Added entity: {entity_id} ({entity_type})")
    
    def add_relationship(
        self,
        from_id: str,
        to_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None
    ):
        """Add relationship between entities."""
        self.graph.add_edge(
            from_id,
            to_id,
            relationship_type=relationship_type,
            **(properties or {})
        )
        self._save_graph()
        logger.debug(f"Added relationship: {from_id} -[{relationship_type}]-> {to_id}")
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity by ID."""
        if entity_id in self.graph:
            return dict(self.graph.nodes[entity_id])
        return None
    
    def search_entities(
        self,
        entity_type: Optional[str] = None,
        division_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for entities."""
        results = []
        
        for node_id, node_data in self.graph.nodes(data=True):
            # Filter by type
            if entity_type and node_data.get('entity_type') != entity_type:
                continue
            
            # Filter by division
            if division_id and node_data.get('division_id') != division_id:
                continue
            
            # Filter by properties
            if properties:
                match = all(
                    node_data.get(k) == v
                    for k, v in properties.items()
                )
                if not match:
                    continue
            
            results.append({'id': node_id, **node_data})
        
        return results
    
    def get_relationships(self, entity_id: str) -> List[Dict[str, Any]]:
        """Get all relationships for an entity."""
        relationships = []
        
        # Outgoing edges
        for _, target, data in self.graph.out_edges(entity_id, data=True):
            relationships.append({
                'from': entity_id,
                'to': target,
                'type': data.get('relationship_type'),
                'properties': data
            })
        
        # Incoming edges
        for source, _, data in self.graph.in_edges(entity_id, data=True):
            relationships.append({
                'from': source,
                'to': entity_id,
                'type': data.get('relationship_type'),
                'properties': data
            })
        
        return relationships
    
    def find_path(self, from_id: str, to_id: str) -> Optional[List[str]]:
        """Find shortest path between entities."""
        try:
            return nx.shortest_path(self.graph, from_id, to_id)
        except nx.NetworkXNoPath:
            return None
    
    def get_neighbors(self, entity_id: str, depth: int = 1) -> List[str]:
        """Get neighboring entities within specified depth."""
        if entity_id not in self.graph:
            return []
        
        neighbors = set()
        current_level = {entity_id}
        
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                # Get successors and predecessors
                next_level.update(self.graph.successors(node))
                next_level.update(self.graph.predecessors(node))
            
            neighbors.update(next_level)
            current_level = next_level
        
        neighbors.discard(entity_id)
        return list(neighbors)
    
    def populate_from_data(self, division_id: str, data: List[Dict[str, Any]]):
        """Populate knowledge graph from ingested data."""
        for record in data:
            # Extract entities (simple heuristic)
            if 'employee_id' in record:
                self.add_entity(
                    entity_id=f"emp_{record['employee_id']}",
                    entity_type='Employee',
                    properties=record,
                    division_id=division_id
                )
            elif 'customer_id' in record:
                self.add_entity(
                    entity_id=f"cust_{record['customer_id']}",
                    entity_type='Customer',
                    properties=record,
                    division_id=division_id
                )
            elif 'product_id' in record:
                self.add_entity(
                    entity_id=f"prod_{record['product_id']}",
                    entity_type='Product',
                    properties=record,
                    division_id=division_id
                )
        
        logger.info(f"Populated graph with {len(data)} entities")


__all__ = ['KnowledgeGraphManager']
