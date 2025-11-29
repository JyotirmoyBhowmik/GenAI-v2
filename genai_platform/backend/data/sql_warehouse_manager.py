"""
GenAI Platform - SQL Warehouse Manager
Advanced SQL operations with division partitioning and security filtering
"""

import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from loguru import logger


class SQLWarehouseManager:
    """Manages SQL warehouse with division partitioning and query security."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize SQL warehouse manager."""
        if db_path is None:
            db_path = Path.cwd() / "data" / "warehouse.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_tables()
        
        logger.info("SQLWarehouseManager initialized")
    
    def _init_tables(self):
        """Initialize warehouse tables."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Query analytics table with partitioning
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT NOT NULL,
                division_id TEXT NOT NULL,
                department_id TEXT,
                query_text TEXT,
                model_id TEXT,
                tokens_used INTEGER,
                cost REAL,
                response_time_ms INTEGER,
                status TEXT,
                CONSTRAINT partition_key CHECK (division_id IN ('fmcg', 'manufacturing', 'hotel', 'stationery', 'retail', 'corporate'))
            )
        """)
        
        # Create indexes for partitioning
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_division_timestamp 
            ON query_analytics(division_id, timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_division 
            ON query_analytics(user_id, division_id)
        """)
        
        # Data access log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT NOT NULL,
                division_id TEXT NOT NULL,
                department_id TEXT,
                resource_type TEXT,
                resource_id TEXT,
                action TEXT,
                status TEXT,
                pii_detected BOOLEAN DEFAULT 0
            )
        """)
        
        # User sessions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                division_id TEXT NOT NULL,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                queries_count INTEGER DEFAULT 0,
                total_cost REAL DEFAULT 0.0
            )
        """)
        
        conn.commit()
        conn.close()
        
        logger.debug("Warehouse tables initialized")
    
    def log_query(
        self,
        user_id: str,
        division_id: str,
        department_id: str,
        query_text: str,
        model_id: str,
        tokens_used: int,
        cost: float,
        response_time_ms: int,
        status: str = "success"
    ):
        """Log query analytics."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO query_analytics 
            (user_id, division_id, department_id, query_text, model_id, tokens_used, cost, response_time_ms, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, division_id, department_id, query_text, model_id, tokens_used, cost, response_time_ms, status))
        
        conn.commit()
        conn.close()
        
        logger.debug(f"Logged query for {user_id}")
    
    def query_with_security(
        self,
        sql: str,
        user_id: str,
        division_id: str,
        role_id: str
    ) -> List[Tuple]:
        """
        Execute query with security filtering.
        
        Automatically adds division filtering based on user's division.
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Add division filter if not present
        if 'WHERE' in sql.upper():
            filtered_sql = f"{sql} AND division_id = ?"
        else:
            filtered_sql = f"{sql} WHERE division_id = ?"
        
        cursor.execute(filtered_sql, (division_id,))
        results = cursor.fetchall()
        
        conn.close()
        
        logger.debug(f"Executed secure query for {user_id}")
        return results
    
    def get_division_analytics(
        self,
        division_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get analytics for a division."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        query = """
            SELECT 
                COUNT(*) as total_queries,
                SUM(tokens_used) as total_tokens,
                SUM(cost) as total_cost,
                AVG(response_time_ms) as avg_response_time,
                COUNT(DISTINCT user_id) as unique_users
            FROM query_analytics
            WHERE division_id = ?
        """
        
        params = [division_id]
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_queries': result[0] or 0,
            'total_tokens': result[1] or 0,
            'total_cost': result[2] or 0.0,
            'avg_response_time_ms': result[3] or 0,
            'unique_users': result[4] or 0
        }
    
    def partition_data_by_division(self):
        """Create division-specific views for data partitioning."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        divisions = ['fmcg', 'manufacturing', 'hotel', 'stationery', 'retail', 'corporate']
        
        for division in divisions:
            # Create view for division
            cursor.execute(f"""
                CREATE VIEW IF NOT EXISTS {division}_analytics AS
                SELECT * FROM query_analytics WHERE division_id = '{division}'
            """)
        
        conn.commit()
        conn.close()
        
        logger.info("Created division-partitioned views")


__all__ = ['SQLWarehouseManager']
