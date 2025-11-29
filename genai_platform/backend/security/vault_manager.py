"""
GenAI Platform - Vault Integration
Secure secrets management using HashiCorp Vault or encrypted local storage
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path
from cryptography.fernet import Fernet
from loguru import logger


class VaultManager:
    """Manages secure storage of secrets and credentials."""
    
    def __init__(self, vault_path: Optional[str] = None, encryption_key: Optional[bytes] = None):
        """
        Initialize vault manager.
        
        Args:
            vault_path: Path to encrypted vault file
            encryption_key: Encryption key (generated if not provided)
        """
        if vault_path is None:
            vault_path = Path.cwd() / "data" / ".vault" / "secrets.enc"
        
        self.vault_path = Path(vault_path)
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize encryption
        if encryption_key is None:
            key_path = self.vault_path.parent / ".vault_key"
            if key_path.exists():
                with open(key_path, 'rb') as f:
                    encryption_key = f.read()
            else:
                encryption_key = Fernet.generate_key()
                with open(key_path, 'wb') as f:
                    f.write(encryption_key)
                logger.info("Generated new vault encryption key")
        
        self.cipher = Fernet(encryption_key)
        self.secrets: Dict[str, Any] = {}
        self._load_vault()
        
        logger.info("VaultManager initialized")
    
    def _load_vault(self):
        """Load and decrypt vault."""
        if self.vault_path.exists():
            try:
                with open(self.vault_path, 'rb') as f:
                    encrypted_data = f.read()
                
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.secrets = json.loads(decrypted_data.decode())
                
                logger.debug(f"Loaded {len(self.secrets)} secrets from vault")
            except Exception as e:
                logger.error(f"Error loading vault: {e}")
                self.secrets = {}
        else:
            self.secrets = {}
    
    def _save_vault(self):
        """Encrypt and save vault."""
        try:
            # Serialize secrets
            data = json.dumps(self.secrets, indent=2)
            
            # Encrypt
            encrypted_data = self.cipher.encrypt(data.encode())
            
            # Save
            with open(self.vault_path, 'wb') as f:
                f.write(encrypted_data)
            
            logger.debug("Vault saved successfully")
        except Exception as e:
            logger.error(f"Error saving vault: {e}")
    
    def set_secret(self, key: str, value: Any):
        """
        Store a secret.
        
        Args:
            key: Secret key/name
            value: Secret value
        """
        self.secrets[key] = value
        self._save_vault()
        logger.info(f"Secret stored: {key}")
    
    def get_secret(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a secret.
        
        Args:
            key: Secret key
            default: Default value if not found
            
        Returns:
            Secret value or default
        """
        return self.secrets.get(key, default)
    
    def delete_secret(self, key: str) -> bool:
        """Delete a secret."""
        if key in self.secrets:
            del self.secrets[key]
            self._save_vault()
            logger.info(f"Secret deleted: {key}")
            return True
        return False
    
    def list_secrets(self) -> list:
        """List all secret keys (not values)."""
        return list(self.secrets.keys())
    
    def set_connector_credentials(
        self,
        connector_type: str,
        credentials: Dict[str, str]
    ):
        """Store connector credentials."""
        key = f"connector_{connector_type}"
        self.set_secret(key, credentials)
    
    def get_connector_credentials(self, connector_type: str) -> Optional[Dict[str, str]]:
        """Retrieve connector credentials."""
        key = f"connector_{connector_type}"
        return self.get_secret(key)
    
    def set_api_key(self, service: str, api_key: str):
        """Store API key."""
        key = f"api_key_{service}"
        self.set_secret(key, api_key)
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Retrieve API key."""
        key = f"api_key_{service}"
        return self.get_secret(key)


__all__ = ['VaultManager']
