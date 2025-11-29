"""
GenAI Platform - HRMS Connectors Package
DarwinBox, Keka, BambooHR connectors
"""

from backend.connectors.base_connector import MockConnector
from typing import Dict, List, Any, Optional


class DarwinBoxConnector(MockConnector):
    """DarwinBox HRMS Connector (Mock Implementation)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "DarwinBox"
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch employee data (mock)."""
        return [
            {'emp_id': 'E001', 'name': 'Rahul Kumar', 'department': 'Engineering', 'designation': 'Senior Engineer'},
            {'emp_id': 'E002', 'name': 'Priya Sharma', 'department': 'HR', 'designation': 'HR Manager'}
        ]


class KekaConnector(MockConnector):
    """Keka HRMS Connector (Mock Implementation)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "Keka"
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch Keka data (mock)."""
        return [
            {'emp_id': 'K001', 'name': 'Amit Patel', 'leave_balance': 15, 'attendance': '95%'},
            {'emp_id': 'K002', 'name': 'Sneha Reddy', 'leave_balance': 12, 'attendance': '98%'}
        ]


class BambooHRConnector(MockConnector):
    """BambooHR Connector (Mock Implementation)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "BambooHR"
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch BambooHR data (mock)."""
        return [
            {'employee_id': 'B001', 'name': 'Sarah Johnson', 'hire_date': '2022-03-15', 'department': 'Sales'},
            {'employee_id': 'B002', 'name': 'Mike Davis', 'hire_date': '2021-11-20', 'department': 'Marketing'}
        ]


__all__ = ['DarwinBoxConnector', 'KekaConnector', 'BambooHRConnector']
