"""
GenAI Platform - Test Suite
Unit and integration tests for core components
"""

import unittest
from pathlib import Path


class TestConfigManager(unittest.TestCase):
    """Test configuration manager."""
    
    def test_config_loads(self):
        """Test that configuration loads without errors."""
        from backend.config_manager import get_config
        config = get_config()
        self.assertIsNotNone(config)
    
    def test_division_retrieval(self):
        """Test division retrieval."""
        from backend.config_manager import get_config
        config = get_config()
        division = config.get_division('fmcg')
        self.assertIsNotNone(division)
        self.assertEqual(division['id'], 'fmcg')
    
    def test_model_listing(self):
        """Test model listing."""
        from backend.config_manager import get_config
        config = get_config()
        models = config.list_models()
        self.assertGreater(len(models), 0)


class TestUserManager(unittest.TestCase):
    """Test user management."""
    
    def test_user_creation(self):
        """Test creating a user."""
        from backend.mdm.user_manager import UserManager
        um = UserManager()
        
        user = um.get_user_by_username('admin')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'admin')
    
    def test_authentication(self):
        """Test user authentication."""
        from backend.mdm.user_manager import UserManager
        um = UserManager()
        
        user = um.authenticate('admin', 'Admin@123')
        self.assertIsNotNone(user)


class TestRBAC(unittest.TestCase):
    """Test RBAC functionality."""
    
    def test_permission_check(self):
        """Test permission checking."""
        from backend.security.rbac import RBACManager
        rbac = RBACManager()
        
        has_perm = rbac.has_permission('super_admin', 'manage_users')
        self.assertTrue(has_perm)
    
    def test_division_access(self):
        """Test division access control."""
        from backend.security.rbac import RBACManager
        rbac = RBACManager()
        
        can_access = rbac.can_access_division('super_admin', 'fmcg', 'fmcg')
        self.assertTrue(can_access)


class TestPIIDetector(unittest.TestCase):
    """Test PII detection."""
    
    def test_email_detection(self):
        """Test email PII detection."""
        from backend.security.pii_detector import PIIDetector
        detector = PIIDetector()
        
        text = "Contact me at test@example.com"
        detections = detector.detect(text)
        
        self.assertGreater(len(detections), 0)
    
    def test_redaction(self):
        """Test PII redaction."""
        from backend.security.pii_detector import PIIDetector
        detector = PIIDetector()
        
        text = "My email is john@example.com"
        redacted, detections = detector.redact(text)
        
        self.assertNotEqual(text, redacted)
        self.assertGreater(len(detections), 0)


class TestConnectors(unittest.TestCase):
    """Test connector framework."""
    
    def test_base_connector(self):
        """Test base connector."""
        from backend.connectors.base_connector import MockConnector
        
        connector = MockConnector({'name': 'test'})
        self.assertTrue(connector.test_connection())
    
    def test_excel_connector(self):
        """Test Excel connector."""
        from backend.connectors.files import ExcelConnector
        
        connector = ExcelConnector({'file_path': 'nonexistent.xlsx', 'name': 'test'})
        self.assertFalse(connector.test_connection())


class TestModelRouter(unittest.TestCase):
    """Test model routing."""
    
    def test_model_router_init(self):
        """Test model router initialization."""
        from backend.models.model_router import ModelRouter
        
        router = ModelRouter()
        self.assertGreater(len(router.get_available_models()), 0)


class TestQueryProcessor(unittest.TestCase):
    """Test query processing."""
    
    def test_query_processing(self):
        """Test basic query processing."""
        from backend.orchestration.query_processor import QueryProcessor, QueryContext
        
        processor = QueryProcessor()
        context = QueryContext(
            user_id='test',
            division_id='fmcg',
            department_id='sales',
            persona_id='general_assistant',
            role_id='analyst'
        )
        
        response = processor.process("Hello", context)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.text)


class TestBilling(unittest.TestCase):
    """Test billing functionality."""
    
    def test_cost_tracking(self):
        """Test cost tracking."""
        from backend.billing.billing_engine import CostTracker
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tracker = CostTracker(storage_path=str(Path(tmpdir) / "costs.json"))
            
            tracker.record_cost(
                user_id='user1',
                division_id='fmcg',
                department_id='sales',
                model_id='gpt-4',
                tokens_used=100,
                cost=0.05
            )
            
            total = tracker.get_total_cost(user_id='user1')
            self.assertAlmostEqual(total, 0.05)


def run_tests():
    """Run all tests."""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    unittest.main()
