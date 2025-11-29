"""
GenAI Platform - File Connectors Package  
Excel, PDF, Word, CSV file processors
"""

from backend.connectors.base_connector import BaseConnector
from typing import Dict, List, Any, Optional
from pathlib import Path
from loguru import logger
import pandas as pd


class ExcelConnector(BaseConnector):
    """Excel file analyzer and data extractor."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "Excel"
        self.file_path = config.get('file_path')
    
    def connect(self) -> bool:
        """Check if file exists."""
        if self.file_path and Path(self.file_path).exists():
            self.is_connected = True
            self.update_status('connected')
            logger.info(f"Excel file loaded: {self.file_path}")
            return True
        return False
    
    def disconnect(self):
        """Nothing to disconnect for files."""
        self.is_connected = False
        self.update_status('disconnected')
    
    def test_connection(self) -> bool:
        """Test if file is accessible."""
        return self.file_path and Path(self.file_path).exists()
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Read Excel file and return data."""
        if not self.file_path or not Path(self.file_path).exists():
            logger.error(f"Excel file not found: {self.file_path}")
            return []
        
        try:
            # Read Excel file
            df = pd.read_excel(self.file_path)
            
            # Convert to list of dicts
            data = df.to_dict('records')
            
            self.metadata.records_count = len(data)
            logger.info(f"Loaded {len(data)} records from Excel")
            
            return data
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            return []
    
    def get_schema(self) -> Dict[str, Any]:
        """Get column names and types."""
        if not self.file_path or not Path(self.file_path).exists():
            return {}
        
        try:
            df = pd.read_excel(self.file_path, nrows=0)
            return {
                'columns': list(df.columns),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
        except:
            return {}


class CSVConnector(BaseConnector):
    """CSV file processor."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "CSV"
        self.file_path = config.get('file_path')
    
    def connect(self) -> bool:
        """Check if file exists."""
        if self.file_path and Path(self.file_path).exists():
            self.is_connected = True
            self.update_status('connected')
            return True
        return False
    
    def disconnect(self):
        """Nothing to disconnect."""
        self.is_connected = False
        self.update_status('disconnected')
    
    def test_connection(self) -> bool:
        """Test if file exists."""
        return self.file_path and Path(self.file_path).exists()
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Read CSV and return data."""
        if not self.file_path or not Path(self.file_path).exists():
            return []
        
        try:
            df = pd.read_csv(self.file_path)
            data = df.to_dict('records')
            self.metadata.records_count = len(data)
            return data
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            return []
    
    def get_schema(self) -> Dict[str, Any]:
        """Get CSV schema."""
        if not self.file_path or not Path(self.file_path).exists():
            return {}
        
        try:
            df = pd.read_csv(self.file_path, nrows=0)
            return {
                'columns': list(df.columns),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
        except:
            return {}


class PDFConnector(BaseConnector):
    """PDF processor with OCR support."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connector_type = "PDF"
        self.file_path = config.get('file_path')
    
    def connect(self) -> bool:
        """Check if file exists."""
        if self.file_path and Path(self.file_path).exists():
            self.is_connected = True
            self.update_status('connected')
            return True
        return False
    
    def disconnect(self):
        """Nothing to disconnect."""
        self.is_connected = False
    
    def test_connection(self) -> bool:
        """Test if file exists."""
        return self.file_path and Path(self.file_path).exists()
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract text from PDF."""
        if not self.file_path:
            return []
        
        try:
            import PyPDF2
            
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                return[{
                    'file': self.file_path,
                    'pages': len(reader.pages),
                    'text': text,
                    'size': Path(self.file_path).stat().st_size
                }]
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            return [{'file': self.file_path, 'text': 'PDF processing requires PyPDF2', 'error': str(e)}]
    
    def get_schema(self) -> Dict[str, Any]:
        """Get PDF metadata."""
        return {'type': 'PDF', 'fields': ['file', 'pages', 'text', 'size']}


__all__ = ['ExcelConnector', 'CSVConnector', 'PDFConnector']
