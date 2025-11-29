"""
GenAI Platform - Enhanced Testing Suite
Comprehensive tests for all components  
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestVaultManager(unittest.TestCase):
    """Test vault integration."""
    
    def test_vault_init(self):
        """Test vault initialization."""
        from backend.security.vault_manager import VaultManager
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = VaultManager(vault_path=str(Path(tmpdir) / "vault.enc"))
            self.assertIsNotNone(vault)
    
    def test_secret_storage(self):
        """Test storing and retrieving secrets."""
        from backend.security.vault_manager import VaultManager
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = VaultManager(vault_path=str(Path(tmpdir) / "vault.enc"))
            
            vault.set_secret('test_key', 'test_value')
            retrieved = vault.get_secret('test_key')
            
            self.assertEqual(retrieved, 'test_value')


class TestKnowledgeGraph(unittest.TestCase):
    """Test knowledge graph manager."""
    
    def test_entity_creation(self):
        """Test creating entities."""
        from backend.data.knowledge_graph_manager import KnowledgeGraphManager
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            kg = KnowledgeGraphManager(graph_path=str(Path(tmpdir) / "graph.pkl"))
            
            kg.add_entity(
                entity_id='emp_001',
                entity_type='Employee',
                properties={'name': 'John Doe'},
                division_id='fmcg'
            )
            
            entity = kg.get_entity('emp_001')
            self.assertIsNotNone(entity)
            self.assertEqual(entity['entity_type'], 'Employee')
    
    def test_relationships(self):
        """Test entity relationships."""
        from backend.data.knowledge_graph_manager import KnowledgeGraphManager
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            kg = KnowledgeGraphManager(graph_path=str(Path(tmpdir) / "graph.pkl"))
            
            kg.add_entity('emp_001', 'Employee', {}, 'fmcg')
            kg.add_entity('dept_001', 'Department', {}, 'fmcg')
            kg.add_relationship('emp_001', 'dept_001', 'WORKS_IN')
            
            rels = kg.get_relationships('emp_001')
            self.assertGreater(len(rels), 0)


class TestSQLWarehouse(unittest.TestCase):
    """Test SQL warehouse manager."""
    
    def test_query_logging(self):
        """Test query logging."""
        from backend.data.sql_warehouse_manager import SQLWarehouseManager
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            warehouse = SQLWarehouseManager(db_path=str(Path(tmpdir) / "warehouse.db"))
            
            warehouse.log_query(
                user_id='user1',
                division_id='fmcg',
                department_id='sales',
                query_text='test query',
                model_id='gpt-4',
                tokens_used=100,
                cost=0.05,
                response_time_ms=500
            )
            
            analytics = warehouse.get_division_analytics('fmcg')
            self.assertEqual(analytics['total_queries'], 1)


class TestEmbeddingGenerator(unittest.TestCase):
    """Test embedding generation."""
    
    def test_embedding_generation(self):
        """Test generating embeddings."""
        from backend.ingestion.embedding_generator import EmbeddingGenerator
        
        generator = EmbeddingGenerator()
        texts = ["Hello world", "Test text"]
        embeddings = generator.generate(texts)
        
        self.assertEqual(len(embeddings), 2)
        self.assertIsInstance(embeddings[0], list)


class TestGUIDialogs(unittest.TestCase):
    """Test GUI dialog windows."""
    
    def test_billing_dialog_creation(self):
        """Test creating billing stats dialog."""
        try:
            from PyQt6.QtWidgets import QApplication
            from gui.dialogs.additional_windows import BillingStatsDialog
            
            app = QApplication.instance() or QApplication(sys.argv)
            dialog = BillingStatsDialog()
            
            self.assertIsNotNone(dialog)
            self.assertEqual(dialog.windowTitle(), "Billing Statistics")
        except ImportError:
            self.skipTest("PyQt6 not available")


class TestDivisionSegregation(unittest.TestCase):
    """Test division data segregation."""
    
    def test_division_isolation(self):
        """Test that divisions are properly isolated."""
        from backend.security.rbac import RBACManager
        
        rbac = RBACManager()
        
        # Analyst cannot access other divisions
        can_access = rbac.can_access_division(
            role_id='analyst',
            division_id='manufacturing',
            user_division='fmcg'
        )
        
        self.assertFalse(can_access)
    
    def test_cross_division_super_admin(self):
        """Test super admin can access all divisions."""
        from backend.security.rbac import RBACManager
        
        rbac = RBACManager()
        
        can_access = rbac.can_access_division(
            role_id='super_admin',
            division_id='manufacturing',
            user_division='fmcg'
        )
        
        self.assertTrue(can_access)


class TestIntegrationScenarios(unittest.TestCase):
    """End-to-end integration tests."""
    
    def test_full_query_flow(self):
        """Test complete query processing flow."""
        from backend.orchestration.query_processor import QueryProcessor, QueryContext
        
        processor = QueryProcessor()
        context = QueryContext(
            user_id='test_user',
            division_id='fmcg',
            department_id='sales',
            persona_id='general_assistant',
            role_id='analyst'
        )
        
        response = processor.process("Test query", context)
        
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.text)
        self.assertGreaterEqual(response.cost, 0)


def run_comprehensive_tests():
    """Run all tests with detailed output."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    unittest.main()
