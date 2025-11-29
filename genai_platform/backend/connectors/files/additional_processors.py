"""
GenAI Platform - Additional File Processors
Word, Image, and Folder processors
"""

from backend.connectors.base_connector import BaseConnector
from typing import Dict, List, Any, Optional
from pathlib import Path
from loguru import logger


class WordConnector(BaseConnector):
    """Word document processor (mock)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "Word"
        self.file_path = config.get('file_path')
    
    def connect(self) -> bool:
        """Check if file exists."""
        if self.file_path and Path(self.file_path).exists():
            self.is_connected = True
            self.update_status('connected')
            return True
        return False
    
    def disconnect(self):
        """Disconnect."""
        self.is_connected = False
    
    def test_connection(self) -> bool:
        """Test if file exists."""
        return self.file_path and Path(self.file_path).exists()
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract text from Word document."""
        # Placeholder - requires python-docx library
        return [{
            'file': self.file_path,
            'text': 'Word document processing requires python-docx library',
            'note': 'Install: pip install python-docx'
        }]
    
    def get_schema(self) -> Dict[str, Any]:
        """Get Word metadata."""
        return {'type': 'Word', 'fields': ['file', 'text', 'metadata']}


class ImageConnector(BaseConnector):
    """Image processor with OCR."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "Image"
        self.file_path = config.get('file_path')
    
    def connect(self) -> bool:
        """Check if file exists."""
        if self.file_path and Path(self.file_path).exists():
            self.is_connected = True
            self.update_status('connected')
            return True
        return False
    
    def disconnect(self):
        """Disconnect."""
        self.is_connected = False
    
    def test_connection(self) -> bool:
        """Test if file exists."""
        return self.file_path and Path(self.file_path).exists()
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract text from image using OCR."""
        # Placeholder - requires PIL and pytesseract
        return [{
            'file': self.file_path,
            'text': 'Image OCR processing requires pytesseract',
            'note': 'Install: pip install pytesseract pillow'
        }]
    
    def get_schema(self) -> Dict[str, Any]:
        """Get image metadata."""
        return {'type': 'Image', 'fields': ['file', 'text', 'dimensions']}


class FolderConnector(BaseConnector):
    """Folder ingestion for batch processing."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "Folder"
        self.folder_path = config.get('folder_path')
    
    def connect(self) -> bool:
        """Check if folder exists."""
        if self.folder_path and Path(self.folder_path).exists():
            self.is_connected = True
            self.update_status('connected')
            return True
        return False
    
    def disconnect(self):
        """Disconnect."""
        self.is_connected = False
    
    def test_connection(self) -> bool:
        """Test if folder exists."""
        return self.folder_path and Path(self.folder_path).exists()
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List all files in folder."""
        if not self.folder_path or not Path(self.folder_path).exists():
            return []
        
        files = []
        folder = Path(self.folder_path)
        
        for file_path in folder.rglob('*'):
            if file_path.is_file():
                files.append({
                    'file_path': str(file_path),
                    'file_name': file_path.name,
                    'file_type': file_path.suffix,
                    'size': file_path.stat().st_size,
                    'modified': file_path.stat().st_mtime
                })
        
        self.metadata.records_count = len(files)
        return files
    
    def get_schema(self) -> Dict[str, Any]:
        """Get folder metadata."""
        return {
            'type': 'Folder',
            'fields': ['file_path', 'file_name', 'file_type', 'size', 'modified']
        }


__all__ = ['WordConnector', 'ImageConnector', 'FolderConnector']
