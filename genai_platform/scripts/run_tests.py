"""
GenAI Platform - Test Runner Script
Runs all tests and generates report
"""

import sys
import unittest
from pathlib import Path
from loguru import logger


def run_all_tests():
    """Run all tests in the tests directory."""
    # Configure logger
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    
    logger.info("="*60)
    logger.info("GenAI Platform - Test Suite")
    logger.info("="*60)
    
    # Add project root to path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Discover tests
    loader = unittest.TestLoader()
    tests_dir = project_root / "tests"
    
    if not tests_dir.exists():
        logger.error(f"Tests directory not found: {tests_dir}")
        return False
    
    logger.info(f"Discovering tests in: {tests_dir}")
    suite = loader.discover(start_dir=str(tests_dir), pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    logger.info("="*60)
    logger.info("Test Summary")
    logger.info("="*60)
    logger.info(f"Tests run: {result.testsRun}")
    logger.info(f"Failures: {len(result.failures)}")
    logger.info(f"Errors: {len(result.errors)}")
    logger.info(f"Skipped: {len(result.skipped)}")
    logger.info("="*60)
    
    if result.wasSuccessful():
        logger.info("✓ All tests passed!")
        return True
    else:
        logger.error("✗ Some tests failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
