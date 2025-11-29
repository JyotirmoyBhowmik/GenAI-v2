"""
GenAI Platform - Consent Management System
GDPR-compliant user consent tracking
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger


class ConsentManager:
    """Manages user consent for data processing and compliance."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """Initialize consent manager."""
        if storage_path is None:
            storage_path = Path.cwd() / "data" / "consent" / "consents.json"
        
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.consents: List[Dict[str, Any]] = []
        self._load_consents()
        
        logger.info("ConsentManager initialized")
    
    def _load_consents(self):
        """Load consents from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    self.consents = json.load(f)
            except:
                self.consents = []
    
    def _save_consents(self):
        """Save consents to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.consents, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving consents: {e}")
    
    def record_consent(
        self,
        user_id: str,
        consent_type: str,
        purpose: str,
        granted: bool,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record user consent.
        
        Args:
            user_id: User ID
            consent_type: Type of consent (data_processing, marketing, analytics, etc.)
            purpose: Purpose description
            granted: Whether consent was granted
            metadata: Additional metadata
            
        Returns:
            Consent ID
        """
        consent_id = f"CONSENT-{len(self.consents) + 1:06d}"
        
        consent = {
            'consent_id': consent_id,
            'user_id': user_id,
            'consent_type': consent_type,
            'purpose': purpose,
            'granted': granted,
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': metadata or {}
        }
        
        self.consents.append(consent)
        self._save_consents()
        
        logger.info(f"Consent recorded: {consent_id} for user {user_id}")
        return consent_id
    
    def revoke_consent(self, user_id: str, consent_type: str) -> bool:
        """Revoke user consent."""
        for consent in self.consents:
            if consent['user_id'] == user_id and consent['consent_type'] == consent_type:
                consent['granted'] = False
                consent['revoked_at'] = datetime.utcnow().isoformat()
        
        self._save_consents()
        logger.info(f"Consent revoked for user {user_id}, type {consent_type}")
        return True
    
    def has_consent(self, user_id: str, consent_type: str) -> bool:
        """Check if user has given consent."""
        for consent in self.consents:
            if (consent['user_id'] == user_id and 
                consent['consent_type'] == consent_type and 
                consent['granted'] and 
                'revoked_at' not in consent):
                return True
        return False
    
    def get_user_consents(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all consents for a user."""
        return [c for c in self.consents if c['user_id'] == user_id]


__all__ = ['ConsentManager']
