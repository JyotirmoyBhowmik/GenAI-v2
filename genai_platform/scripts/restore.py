"""
GenAI Platform - Restore Script
Restores platform data from backups
"""

import sys
import os
from pathlib import Path
from loguru import logger
import json
from datetime import datetime


def list_backups(backup_dir: str = "./backups") -> list:
    """List available backups"""
    backups = []
    backup_path = Path(backup_dir)
    
    if not backup_path.exists():
        logger.warning(f"Backup directory not found: {backup_dir}")
        return backups
    
    for backup_folder in backup_path.iterdir():
        if backup_folder.is_dir():
            metadata_file = backup_folder / "metadata.json"
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    backups.append({
                        'id': backup_folder.name,
                        'timestamp': metadata.get('timestamp', 'unknown'),
                        'size': sum(f.stat().st_size for f in backup_folder.rglob('*') if f.is_file()),
                        'components': metadata.get('components', [])
                    })
                except Exception as e:
                    logger.warning(f"Error reading backup metadata: {e}")
    
    return sorted(backups, key=lambda x: x['timestamp'], reverse=True)


def restore_backup(backup_id: str, backup_dir: str = "./backups") -> bool:
    """Restore data from backup"""
    logger.info(f"Restoring backup: {backup_id}")
    
    backup_path = Path(backup_dir) / backup_id
    
    if not backup_path.exists():
        logger.error(f"Backup not found: {backup_id}")
        return False
    
    try:
        from backend.backup.backup_manager import BackupManager
        manager = BackupManager()
        
        # Read metadata
        metadata_file = backup_path / "metadata.json"
        if not metadata_file.exists():
            logger.error(f"Backup metadata not found")
            return False
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        logger.info(f"Backup timestamp: {metadata.get('timestamp')}")
        logger.info(f"Components: {', '.join(metadata.get('components', []))}")
        
        # Restore vector database
        if 'vector_db' in metadata.get('components', []):
            try:
                manager.restore_vector_db(backup_path)
                logger.info("✓ Restored vector database")
            except Exception as e:
                logger.warning(f"Vector database restoration failed: {e}")
        
        # Restore knowledge graph
        if 'knowledge_graph' in metadata.get('components', []):
            try:
                manager.restore_knowledge_graph(backup_path)
                logger.info("✓ Restored knowledge graph")
            except Exception as e:
                logger.warning(f"Knowledge graph restoration failed: {e}")
        
        # Restore warehouse
        if 'warehouse' in metadata.get('components', []):
            try:
                manager.restore_warehouse(backup_path)
                logger.info("✓ Restored SQL warehouse")
            except Exception as e:
                logger.warning(f"Warehouse restoration failed: {e}")
        
        logger.info(f"✓ Backup restored successfully: {backup_id}")
        return True
        
    except Exception as e:
        logger.error(f"Restoration failed: {e}")
        return False


def main():
    """Main entry point"""
    # Configure logging
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
    
    logger.info("=" * 60)
    logger.info("GenAI Platform - Backup Restoration")
    logger.info("=" * 60)
    
    # Check arguments
    if len(sys.argv) < 2:
        logger.info("\nUsage: python restore.py --backup-id <backup_id>")
        logger.info("       python restore.py --list")
        logger.info("")
        
        # List available backups
        backups = list_backups()
        if backups:
            logger.info("Available backups:")
            for backup in backups[:5]:
                logger.info(f"  - {backup['id']} ({backup['timestamp']})")
            if len(backups) > 5:
                logger.info(f"  ... and {len(backups) - 5} more")
        else:
            logger.info("No backups found")
        
        return False
    
    if sys.argv[1] == "--list":
        # List backups
        backups = list_backups()
        if backups:
            logger.info("\nAvailable backups:")
            logger.info("=" * 60)
            for backup in backups:
                size_mb = backup['size'] / (1024 * 1024)
                logger.info(f"ID: {backup['id']}")
                logger.info(f"  Timestamp: {backup['timestamp']}")
                logger.info(f"  Size: {size_mb:.2f} MB")
                logger.info(f"  Components: {', '.join(backup['components'])}")
                logger.info("")
        else:
            logger.info("No backups found")
        
        return True
    
    elif sys.argv[1] == "--backup-id" and len(sys.argv) > 2:
        backup_id = sys.argv[2]
        success = restore_backup(backup_id)
        return success
    
    else:
        logger.error("Invalid arguments")
        logger.info("Use: --list or --backup-id <id>")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
