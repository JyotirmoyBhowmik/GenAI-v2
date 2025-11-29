"""
GenAI Platform - Billing Engine
Tracks costs and generates billing reports
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger


class CostTracker:
    """Tracks usage costs at user/department/division levels."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize cost tracker.
        
        Args:
            storage_path: Path to cost tracking database
        """
        if storage_path is None:
            storage_path = Path.cwd() / "data" / "billing" / "costs.json"
        
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.costs: List[Dict[str, Any]] = []
        self._load_costs()
        
        logger.info("CostTracker initialized")
    
    def _load_costs(self):
        """Load costs from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    self.costs = json.load(f)
                logger.debug(f"Loaded {len(self.costs)} cost records")
            except Exception as e:
                logger.error(f"Error loading costs: {e}")
                self.costs = []
        else:
            self.costs = []
    
    def _save_costs(self):
        """Save costs to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.costs, f, indent=2)
            logger.debug(f"Saved {len(self.costs)} cost records")
        except Exception as e:
            logger.error(f"Error saving costs: {e}")
    
    def record_cost(
        self,
        user_id: str,
        division_id: str,
        department_id: str,
        model_id: str,
        tokens_used: int,
        cost: float,
        operation_type: str = "query"
    ):
        """
        Record a cost entry.
        
        Args:
            user_id: User ID
            division_id: Division ID
            department_id: Department ID
            model_id: Model used
            tokens_used: Number of tokens
            cost: Cost in USD
            operation_type: Type of operation (query, ingestion, etc.)
        """
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'division_id': division_id,
            'department_id': department_id,
            'model_id': model_id,
            'tokens_used': tokens_used,
            'cost': cost,
            'operation_type': operation_type
        }
        
        self.costs.append(entry)
        self._save_costs()
        
        logger.debug(f"Recorded cost: ${cost:.4f} for {model_id}")
    
    def get_costs(
        self,
        user_id: Optional[str] = None,
        division_id: Optional[str] = None,
        department_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get filtered costs.
        
        Args:
            user_id: Filter by user
            division_id: Filter by division
            department_id: Filter by department
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            
        Returns:
            Filtered cost records
        """
        filtered = self.costs
        
        if user_id:
            filtered = [c for c in filtered if c.get('user_id') == user_id]
        
        if division_id:
            filtered = [c for c in filtered if c.get('division_id') == division_id]
        
        if department_id:
            filtered = [c for c in filtered if c.get('department_id') == department_id]
        
        if start_date:
            filtered = [c for c in filtered if c.get('timestamp', '') >= start_date]
        
        if end_date:
            filtered = [c for c in filtered if c.get('timestamp', '') <= end_date]
        
        return filtered
    
    def get_total_cost(self, **filters) -> float:
        """Get total cost with filters."""
        costs = self.get_costs(**filters)
        return sum(c.get('cost', 0) for c in costs)
    
    def get_stats(self, **filters) -> Dict[str, Any]:
        """Get cost statistics."""
        costs = self.get_costs(**filters)
        
        if not costs:
            return {
                'total_cost': 0,
                'total_tokens': 0,
                'query_count': 0,
                'avg_cost_per_query': 0
            }
        
        total_cost = sum(c.get('cost', 0) for c in costs)
        total_tokens = sum(c.get('tokens_used', 0) for c in costs)
        
        return {
            'total_cost': total_cost,
            'total_tokens': total_tokens,
            'query_count': len(costs),
            'avg_cost_per_query': total_cost / len(costs) if costs else 0,
            'avg_tokens_per_query': total_tokens / len(costs) if costs else 0
        }


class BillingEngine:
    """Generates billing reports and invoices."""
    
    def __init__(self, cost_tracker: CostTracker):
        """
        Initialize billing engine.
        
        Args:
            cost_tracker: CostTracker instance
        """
        self.cost_tracker = cost_tracker
        logger.info("BillingEngine initialized")
    
    def generate_user_report(self, user_id: str, month: Optional[str] = None) -> Dict[str, Any]:
        """Generate billing report for a user."""
        if not month:
            # Current month
            now = datetime.utcnow()
            start_date = now.replace(day=1).isoformat()
            end_date = now.isoformat()
        else:
            # Specific month (format: YYYY-MM)
            start_date = f"{month}-01T00:00:00"
            # Calculate end of month
            year, month_num = month.split('-')
            if int(month_num) == 12:
                end_date = f"{int(year)+1}-01-01T00:00:00"
            else:
                end_date = f"{year}-{int(month_num)+1:02d}-01T00:00:00"
        
        costs = self.cost_tracker.get_costs(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        stats = self.cost_tracker.get_stats(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Group by model
        by_model = {}
        for cost in costs:
            model = cost.get('model_id', 'unknown')
            if model not in by_model:
                by_model[model] = {'cost': 0, 'tokens': 0, 'count': 0}
            by_model[model]['cost'] += cost.get('cost', 0)
            by_model[model]['tokens'] += cost.get('tokens_used', 0)
            by_model[model]['count'] += 1
        
        return {
            'user_id': user_id,
            'period': f"{start_date} to {end_date}",
            'summary': stats,
            'by_model': by_model,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def generate_division_report(self, division_id: str, month: Optional[str] = None) -> Dict[str, Any]:
        """Generate billing report for a division."""
        if not month:
            now = datetime.utcnow()
            start_date = now.replace(day=1).isoformat()
            end_date = now.isoformat()
        else:
            start_date = f"{month}-01T00:00:00"
            year, month_num = month.split('-')
            if int(month_num) == 12:
                end_date = f"{int(year)+1}-01-01T00:00:00"
            else:
                end_date = f"{year}-{int(month_num)+1:02d}-01T00:00:00"
        
        costs = self.cost_tracker.get_costs(
            division_id=division_id,
            start_date=start_date,
            end_date=end_date
        )
        
        stats = self.cost_tracker.get_stats(
            division_id=division_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Group by department
        by_department = {}
        for cost in costs:
            dept = cost.get('department_id', 'unknown')
            if dept not in by_department:
                by_department[dept] = {'cost': 0, 'tokens': 0, 'count': 0}
            by_department[dept]['cost'] += cost.get('cost', 0)
            by_department[dept]['tokens'] += cost.get('tokens_used', 0)
            by_department[dept]['count'] += 1
        
        return {
            'division_id': division_id,
            'period': f"{start_date} to {end_date}",
            'summary': stats,
            'by_department': by_department,
            'generated_at': datetime.utcnow().isoformat()
        }


class InvoiceGenerator:
    """Generates PDF invoices."""
    
    @staticmethod
    def generate_invoice(report: Dict[str, Any], output_path: str):
        """
        Generate PDF invoice from report.
        
        Args:
            report: Billing report dictionary
            output_path: Output PDF path
        """
        # Placeholder - would use reportlab or similar for actual PDF generation
        logger.info(f"Generating invoice: {output_path}")
        
        # For now, save as JSON
        json_path = output_path.replace('.pdf', '.json')
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Invoice saved as JSON: {json_path}")
        logger.info("Note: PDF generation requires reportlab library")
