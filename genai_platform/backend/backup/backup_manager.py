"""
GenAI Platform - Backup Manager
Handles backup and recovery of platform data
"""

import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from loguru import logger


class BackupManager:
    """Manages backups of vector DB, knowledge graph, configurations, and warehouse."""
    
    def __init__(self, backup_dir: str = "./backups"):
        """
        Initialize backup manager.
        
        Args:
            backup_dir: Directory to store backups
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"BackupManager initialized (dir: {self.backup_dir})")
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Create a full backup.
        
        Args:
            backup_name: Optional backup name (default: timestamp)
            
        Returns:
            Backup ID
        """
        if backup_name is None:
            backup_name = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        backup_id = f"backup_{backup_name}"
        backup_path = self.backup_dir / backup_id
        backup_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Creating backup: {backup_id}")
        
        manifest = {
            'backup_id': backup_id,
            'timestamp': datetime.utcnow().isoformat(),
            'components': []
        }
        
        # Backup vector DB
        try:
            vector_db_path = Path("./data/chroma_db")
            if vector_db_path.exists():
                dest = backup_path / "vector_db"
                shutil.copytree(vector_db_path, dest)
                manifest['components'].append('vector_db')
                logger.debug("Backed up vector DB")
        except Exception as e:
            logger.error(f"Error backing up vector DB: {e}")
        
        # Backup knowledge graph
        try:
            kg_path = Path("./data/knowledge_graph")
            if kg_path.exists():
                dest = backup_path / "knowledge_graph"
                shutil.copytree(kg_path, dest)
                manifest['components'].append('knowledge_graph')
                logger.debug("Backed up knowledge graph")
        except Exception as e:
            logger.error(f"Error backing up knowledge graph: {e}")
        
        # Backup SQL warehouse
        try:
            warehouse_path = Path("./data/warehouse.db")
            if warehouse_path.exists():
                dest = backup_path / "warehouse.db"
                shutil.copy2(warehouse_path, dest)
                manifest['components'].append('warehouse')
                logger.debug("Backed up SQL warehouse")
        except Exception as e:
            logger.error(f"Error backing up warehouse: {e}")
        
        # Backup configurations
        try:
            config_path = Path("./config")
            if config_path.exists():
                dest = backup_path / "config"
                shutil.copytree(config_path, dest)
                manifest['components'].append('config')
                logger.debug("Backed up configurations")
        except Exception as e:
            logger.error(f"Error backing up config: {e}")
        
        # Backup MDM data
        try:
            mdm_path = Path("./data/mdm")
            if mdm_path.exists():
                dest = backup_path / "mdm"
                shutil.copytree(mdm_path, dest)
                manifest['components'].append('mdm')
                logger.debug("Backed up MDM data")
        except Exception as e:
            logger.error(f"Error backing up MDM: {e}")
        
        # Save manifest
        manifest_path = backup_path / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Backup created successfully: {backup_id}")
        logger.info(f"Components: {', '.join(manifest['components'])}")
        
        return backup_id
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups."""
        backups = []
        
        for backup_path in self.backup_dir.iterdir():
            if backup_path.is_dir() and backup_path.name.startswith('backup_'):
                manifest_path = backup_path / "manifest.json"
                
                if manifest_path.exists():
                    try:
                        with open(manifest_path, 'r') as f:
                            manifest = json.load(f)
                        backups.append(manifest)
                    except:
                        pass
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return backups
    
    def delete_backup(self, backup_id: str) -> bool:
        """
        Delete a backup.
        
        Args:
            backup_id: Backup ID to delete
            
        Returns:
            True if successful
        """
        backup_path = self.backup_dir / backup_id
        
        if not backup_path.exists():
            logger.error(f"Backup not found: {backup_id}")
            return False
        
        try:
            shutil.rmtree(backup_path)
            logger.info(f"Deleted backup: {backup_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting backup: {e}")
            return False


class RestoreManager:
    """Manages restoration from backups."""
    
    def __init__(self, backup_dir: str = "./backups"):
        """
        Initialize restore manager.
        
        Args:
            backup_dir: Backup directory
        """
        self.backup_dir = Path(backup_dir)
        logger.info("RestoreManager initialized")
    
    def restore_backup(self, backup_id: str, components: Optional[List[str]] = None) -> bool:
        """
        Restore from a backup.
        
        Args:
            backup_id: Backup ID to restore
            components: List of components to restore (None = all)
            
        Returns:
            True if successful
        """
        backup_path = self.backup_dir / backup_id
        
        if not backup_path.exists():
            logger.error(f"Backup not found: {backup_id}")
            return False
        
        # Load manifest
        manifest_path = backup_path / "manifest.json"
        if not manifest_path.exists():
            logger.error("Backup manifest not found")
            return False
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        available_components = manifest.get('components', [])
        
        if components is None:
            components = available_components
        
        logger.info(f"Restoring backup: {backup_id}")
        logger.info(f"Components: {', '.join(components)}")
        
        # Restore each component
        for component in components:
            if component not in available_components:
                logger.warning(f"Component not in backup: {component}")
                continue
            
            try:
                if component == 'vector_db':
                    src = backup_path / "vector_db"
                    dest = Path("./data/chroma_db")
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(src, dest)
                    logger.debug("Restored vector DB")
                
                elif component == 'knowledge_graph':
                    src = backup_path / "knowledge_graph"
                    dest = Path("./data/knowledge_graph")
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(src, dest)
                    logger.debug("Restored knowledge graph")
                
                elif component == 'warehouse':
                    src = backup_path / "warehouse.db"
                    dest = Path("./data/warehouse.db")
                    if dest.exists():
                        dest.unlink()
                    shutil.copy2(src, dest)
                    logger.debug("Restored warehouse")
                
                elif component == 'config':
                    src = backup_path / "config"
                    dest = Path("./config")
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(src, dest)
                    logger.debug("Restored configurations")
                
                elif component == 'mdm':
                    src = backup_path / "mdm"
                    dest = Path("./data/mdm")
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(src, dest)
                    logger.debug("Restored MDM data")
                
            except Exception as e:
                logger.error(f"Error restoring {component}: {e}")
                return False
        
        logger.info(f"Restore completed successfully: {backup_id}")
        return True
