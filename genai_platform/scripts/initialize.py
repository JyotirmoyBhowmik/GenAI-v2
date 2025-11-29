"""
GenAI Platform - Initialization Script
Sets up the platform for first-time use
"""

import os
import sys
from pathlib import Path
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_directory_structure():
    """Create all required directories."""
    logger.info("Creating directory structure...")
    
    directories = [
        # Data directories
        "data/chroma_db",
        "data/knowledge_graph",
        "data/warehouse",
        "data/mdm",
        "data/divisions/fmcg",
        "data/divisions/manufacturing",
        "data/divisions/hotel",
        "data/divisions/stationery",
        "data/divisions/retail",
        "data/divisions/corporate",
        "data/shared",
        "data/mock_erp",
        "data/mock_crm",
        "data/mock_hrms",
        "data/cache",
        
        # Logs
        "logs",
        
        # Backups
        "backups",
        
        # Plugins
        "backend/plugins/custom",
    ]
    
    for directory in directories:
        path = project_root / directory
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created directory: {path}")
    
    logger.info("Directory structure created successfully")


def initialize_mdm():
    """Initialize Master Data Management."""
    logger.info("Initializing MDM...")
    
    from backend.mdm.user_manager import UserManager
    
    # Initialize user manager (creates default users)
    user_manager = UserManager()
    logger.info(f"User manager initialized with {len(user_manager.users)} users")


def initialize_vector_db():
    """Initialize vector database."""
    logger.info("Initializing vector database...")
    
    try:
        import chromadb
        from chromadb.config import Settings
        
        # Initialize Chroma with persistence
        persist_dir = str(project_root / "data" / "chroma_db")
        client = chromadb.Client(Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        ))
        
        # Create default collections for each division
        divisions = ["fmcg", "manufacturing", "hotel", "stationery", "retail", "corporate"]
        for division in divisions:
            try:
                collection = client.get_or_create_collection(
                    name=f"genai_platform_{division}",
                    metadata={"division": division}
                )
                logger.debug(f"Created collection for division: {division}")
            except Exception as e:
                logger.warning(f"Error creating collection for {division}: {e}")
        
        logger.info("Vector database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing vector database: {e}")


def initialize_knowledge_graph():
    """Initialize knowledge graph."""
    logger.info("Initializing knowledge graph...")
    
    try:
        import networkx as nx
        import pickle
        
        # Create a simple graph
        G = nx.MultiDiGraph()
        
        # Save to persistence directory
        kg_dir = project_root / "data" / "knowledge_graph"
        kg_dir.mkdir(parents=True, exist_ok=True)
        
        with open(kg_dir / "graph.pkl", 'wb') as f:
            pickle.dump(G, f)
        
        logger.info("Knowledge graph initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing knowledge graph: {e}")


def initialize_warehouse():
    """Initialize SQL warehouse."""
    logger.info("Initializing SQL warehouse...")
    
    try:
        import sqlite3
        
        db_path = project_root / "data" / "warehouse.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create sample tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                division_id TEXT,
                department_id TEXT,
                query TEXT,
                model_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingestion_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                division_id TEXT,
                source_type TEXT,
                source_name TEXT,
                records_count INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        logger.info("SQL warehouse initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing warehouse: {e}")


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_path = project_root / ".env"
    template_path = project_root / ".env.template"
    
    if not env_path.exists() and template_path.exists():
        logger.info("Creating .env file from template...")
        import shutil
        shutil.copy(template_path, env_path)
        logger.info(".env file created. Please edit it with your API keys and settings.")
    else:
        logger.info(".env file already exists")


def verify_configuration():
    """Verify that all configuration files are present."""
    logger.info("Verifying configuration...")
    
    config_files = [
        "config/app_config.yaml",
        "config/divisions.yaml",
        "config/models.yaml",
        "config/personas.yaml",
        "config/policies.yaml"
    ]
    
    all_present = True
    for config_file in config_files:
        path = project_root / config_file
        if not path.exists():
            logger.error(f"Missing configuration file: {config_file}")
            all_present = False
        else:
            logger.debug(f"Found configuration file: {config_file}")
    
    if all_present:
        logger.info("All configuration files present")
    else:
        logger.error("Some configuration files are missing!")
        return False
    
    return True


def main():
    """Main initialization function."""
    logger.info("=" * 60)
    logger.info("GenAI Platform - Initialization")
    logger.info("=" * 60)
    
    try:
        # Step 1: Create directory structure
        create_directory_structure()
        
        # Step 2: Verify configuration
        if not verify_configuration():
            logger.error("Configuration verification failed. Please check config files.")
            return False
        
        # Step 3: Create .env file
        create_env_file()
        
        # Step 4: Initialize MDM
        initialize_mdm()
        
        # Step 5: Initialize vector database
        initialize_vector_db()
        
        # Step 6: Initialize knowledge graph
        initialize_knowledge_graph()
        
        # Step 7: Initialize SQL warehouse
        initialize_warehouse()
        
        logger.info("=" * 60)
        logger.info("✓ Initialization completed successfully!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Edit .env file with your API keys")
        logger.info("2. Install Ollama for local models (optional): https://ollama.ai")
        logger.info("3. Install Tesseract OCR for PDF processing (optional)")
        logger.info("4. Run GUI: python gui/main_window.py")
        logger.info("")
        
        return True
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Configure logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
    logger.add("logs/initialization.log", rotation="10 MB", level="DEBUG")
    
    success = main()
    sys.exit(0 if success else 1)
