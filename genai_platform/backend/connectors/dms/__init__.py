"""
GenAI Platform - DMS Connectors Package
SharePoint Online, OneDrive, Google Drive connectors
"""

from backend.connectors.base_connector import MockConnector
from typing import Dict, List, Any, Optional


class SharePointConnector(MockConnector):
    """SharePoint Online Connector (Mock Implementation)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "SharePoint_Online"
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch SharePoint files and folders (mock)."""
        return [
            {'file_id': 'SP001', 'name': 'Q4_Report.xlsx', 'type': 'file', 'site': 'Finance', 'modified': '2024-01-15'},
            {'file_id': 'SP002', 'name': 'Policy_Document.pdf', 'type': 'file', 'site': 'HR', 'modified': '2024-01-14'},
            {'folder_id': 'SPF001', 'name': 'Shared Documents', 'type': 'folder', 'site': 'Projects'}
        ]


class OneDriveConnector(MockConnector):
    """OneDrive Connector (Mock Implementation)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "OneDrive"
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch OneDrive files (mock)."""
        return [
            {'file_id': 'OD001', 'name': 'Presentation.pptx', 'size': 2048576, 'modified': '2024-01-16'},
            {'file_id': 'OD002', 'name': 'Budget_2024.xlsx', 'size': 512000, 'modified': '2024-01-15'}
        ]


class GoogleDriveConnector(MockConnector):
    """Google Drive Connector (Mock Implementation)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "Google_Drive"
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch Google Drive files (mock)."""
        return [
            {'file_id': 'GD001', 'name': 'Team_Goals.gdoc', 'type': 'document', 'owner': 'user@example.com'},
            {'file_id': 'GD002', 'name': 'Sales_Data.gsheet', 'type': 'spreadsheet', 'owner': 'admin@example.com'}
        ]


__all__ = ['SharePointConnector', 'OneDriveConnector', 'GoogleDriveConnector']
