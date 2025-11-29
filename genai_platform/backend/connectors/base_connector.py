"""
GenAI Platform - Base Connector
Abstract base class for all data source connectors
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from loguru import logger


@dataclass
class ConnectorMetadata:
    """Metadata about a connector."""
    connector_type: str
    source_name: str
    connection_status: str
    last_sync: Optional[str] = None
    records_count: int = 0
    config: Dict[str, Any] = None


class BaseConnector(ABC):
    """
    Abstract base class for all connectors.
    Provides unified interface for connecting to various data sources.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize connector.
        
        Args:
            config: Connector configuration
        """
        self.config = config
        self.connector_type = self.__class__.__name__
        self.is_connected = False
        self.metadata = ConnectorMetadata(
            connector_type=self.connector_type,
            source_name=config.get('name', 'Unknown'),
            connection_status='disconnected',
            config=config
        )
        
        logger.debug(f"Initialized {self.connector_type}")
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to data source.
        
        Returns:
            True if connection successful
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close connection to data source."""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test connection without full connection.
        
        Returns:
            True if connection test successful
        """
        pass
    
    @abstractmethod
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Fetch data from source.
        
        Args:
            query: Query parameters (connector-specific)
            
        Returns:
            List of records as dictionaries
        """
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Get schema/structure of data source.
        
        Returns:
            Schema information
        """
        pass
    
    def get_metadata(self) -> ConnectorMetadata:
        """Get connector metadata."""
        return self.metadata
    
    def update_status(self, status: str):
        """Update connection status."""
        self.metadata.connection_status = status
        self.metadata.last_sync = datetime.utcnow().isoformat()
        logger.debug(f"{self.connector_type} status: {status}")


class MockConnector(BaseConnector):
    """
    Mock connector for testing and demonstration.
    Returns sample data without requiring actual connections.
    """
    
    def connect(self) -> bool:
        """Simulate connection."""
        logger.info(f"Mock connection to {self.config.get('name')}")
        self.is_connected = True
        self.update_status('connected')
        return True
    
    def disconnect(self):
        """Simulate disconnection."""
        logger.info(f"Mock disconnection from {self.config.get('name')}")
        self.is_connected = False
        self.update_status('disconnected')
    
    def test_connection(self) -> bool:
        """Simulate connection test."""
        logger.info(f"Testing mock connection to {self.config.get('name')}")
        return True
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Return mock data."""
        sample_data = [
            {
                'id': '1',
                'type': self.connector_type,
                'source': self.config.get('name'),
                'data': f'Sample record 1 from {self.connector_type}',
                'timestamp': datetime.utcnow().isoformat()
            },
            {
                'id': '2',
                'type': self.connector_type,
                'source': self.config.get('name'),
                'data': f'Sample record 2 from {self.connector_type}',
                'timestamp': datetime.utcnow().isoformat()
            }
        ]
        
        self.metadata.records_count = len(sample_data)
        return sample_data
    
    def get_schema(self) -> Dict[str, Any]:
        """Return mock schema."""
        return {
            'type': self.connector_type,
            'fields': [
                {'name': 'id', 'type': 'string'},
                {'name': 'type', 'type': 'string'},
                {'name': 'source', 'type': 'string'},
                {'name': 'data', 'type': 'string'},
                {'name': 'timestamp', 'type': 'datetime'}
            ]
        }
