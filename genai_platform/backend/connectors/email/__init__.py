"""
GenAI Platform - Email Connectors Package
Outlook 365 and Gmail connectors
"""

from backend.connectors.base_connector import MockConnector
from typing import Dict, List, Any, Optional


class OutlookConnector(MockConnector):
    """Outlook 365 Connector (Mock Implementation)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "Outlook_365"
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch Outlook emails (mock)."""
        return [
            {
                'email_id': 'OUT001',
                'from': 'manager@company.com',
                'to': 'employee@company.com',
                'subject': 'Q4 Performance Review',
                'date': '2024-01-15',
                'has_attachments': True
            },
            {
                'email_id': 'OUT002',
                'from': 'hr@company.com',
                'to': 'all@company.com',
                'subject': 'Updated Leave Policy',
                'date': '2024-01-14',
                'has_attachments': False
            }
        ]


class GmailConnector(MockConnector):
    """Gmail Connector (Mock Implementation)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "Gmail"
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch Gmail messages (mock)."""
        return [
            {
                'message_id': 'GM001',
                'from': 'client@external.com',
                'to': 'sales@company.com',
                'subject': 'Product Inquiry',
                'date': '2024-01-16',
                'labels': ['Inbox', 'Important']
            },
            {
                'message_id': 'GM002',
                'from': 'support@vendor.com',
                'to': 'procurement@company.com',
                'subject': 'Invoice #12345',
                'date': '2024-01-15',
                'labels': ['Inbox']
            }
        ]


__all__ = ['OutlookConnector', 'GmailConnector']
