"""
GenAI Platform - User Manager
Manages user accounts, roles, and permissions
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from loguru import logger
import bcrypt


class User:
    """Represents a user in the system."""
    
    def __init__(
        self,
        user_id: str,
        username: str,
        email: str,
        division_id: str,
        department_id: str,
        role_id: str,
        full_name: str = "",
        enabled: bool = True,
        attributes: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.division_id = division_id
        self.department_id = department_id
        self.role_id = role_id
        self.full_name = full_name
        self.enabled = enabled
        self.attributes = attributes or {}
        self.created_at = datetime.utcnow().isoformat()
        self.last_login = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'division_id': self.division_id,
            'department_id': self.department_id,
            'role_id': self.role_id,
            'full_name': self.full_name,
            'enabled': self.enabled,
            'attributes': self.attributes,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create user from dictionary."""
        user = cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            division_id=data['division_id'],
            department_id=data['department_id'],
            role_id=data['role_id'],
            full_name=data.get('full_name', ''),
            enabled=data.get('enabled', True),
            attributes=data.get('attributes', {})
        )
        user.created_at = data.get('created_at', user.created_at)
        user.last_login = data.get('last_login')
        return user


class UserManager:
    """
    Manages user accounts, authentication, and permissions.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize user manager.
        
        Args:
            storage_path: Path to user storage file (JSON)
        """
        if storage_path is None:
            storage_path = Path.cwd() / "data" / "mdm" / "users.json"
        
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.users: Dict[str, User] = {}
        self.passwords: Dict[str, bytes] = {}  # username -> hashed password
        
        self._load_users()
        logger.info(f"UserManager initialized with {len(self.users)} users")
    
    def _load_users(self):
        """Load users from storage."""
        if not self.storage_path.exists():
            self._create_default_users()
            self._save_users()
            return
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for user_data in data.get('users', []):
                user = User.from_dict(user_data)
                self.users[user.user_id] = user
            
            # Load passwords (in production, use secure vault)
            self.passwords = data.get('passwords', {})
            
            logger.debug(f"Loaded {len(self.users)} users from {self.storage_path}")
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            self._create_default_users()
    
    def _save_users(self):
        """Save users to storage."""
        try:
            data = {
                'users': [user.to_dict() for user in self.users.values()],
                'passwords': self.passwords
            }
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Saved {len(self.users)} users to {self.storage_path}")
        except Exception as e:
            logger.error(f"Error saving users: {e}")
    
    def _create_default_users(self):
        """Create default users for testing."""
        default_users = [
            {
                'username': 'admin',
                'email': 'admin@genai.com',
                'division_id': 'corporate',
                'department_id': 'corp_admin',
                'role_id': 'super_admin',
                'full_name': 'System Administrator',
                'password': 'Admin@123'
            },
            {
                'username': 'fmcg_analyst',
                'email': 'analyst@fmcg.com',
                'division_id': 'fmcg',
                'department_id': 'fmcg_finance',
                'role_id': 'analyst',
                'full_name': 'FMCG Finance Analyst',
                'password': 'Analyst@123'
            },
            {
                'username': 'mfg_viewer',
                'email': 'viewer@manufacturing.com',
                'division_id': 'manufacturing',
                'department_id': 'mfg_production',
                'role_id': 'viewer',
                'full_name': 'Manufacturing Viewer',
                'password': 'Viewer@123'
            }
        ]
        
        for user_data in default_users:
            password = user_data.pop('password')
            user = self.create_user(**user_data)
            self.set_password(user.username, password)
        
        logger.info(f"Created {len(default_users)} default users")
    
    def create_user(
        self,
        username: str,
        email: str,
        division_id: str,
        department_id: str,
        role_id: str,
        full_name: str = "",
        attributes: Optional[Dict[str, Any]] = None
    ) -> User:
        """
        Create a new user.
        
        Args:
            username: Unique username
            email: User email
            division_id: Division ID
            department_id: Department ID
            role_id: Role ID
            full_name: Full name
            attributes: Additional attributes (location, clearance_level, etc.)
            
        Returns:
            Created User object
        """
        user_id = str(uuid.uuid4())
        
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            division_id=division_id,
            department_id=department_id,
            role_id=role_id,
            full_name=full_name,
            attributes=attributes
        )
        
        self.users[user_id] = user
        self._save_users()
        
        logger.info(f"Created user: {username} ({user_id})")
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def update_user(self, user_id: str, **kwargs):
        """Update user attributes."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self._save_users()
        logger.info(f"Updated user: {user_id}")
    
    def delete_user(self, user_id: str):
        """Delete a user."""
        if user_id in self.users:
            username = self.users[user_id].username
            del self.users[user_id]
            if username in self.passwords:
                del self.passwords[username]
            self._save_users()
            logger.info(f"Deleted user: {user_id}")
    
    def list_users(
        self,
        division_id: Optional[str] = None,
        department_id: Optional[str] = None,
        role_id: Optional[str] = None
    ) -> List[User]:
        """
        List users with optional filtering.
        
        Args:
            division_id: Filter by division
            department_id: Filter by department
            role_id: Filter by role
            
        Returns:
            List of User objects
        """
        users = list(self.users.values())
        
        if division_id:
            users = [u for u in users if u.division_id == division_id]
        
        if department_id:
            users = [u for u in users if u.department_id == department_id]
        
        if role_id:
            users = [u for u in users if u.role_id == role_id]
        
        return users
    
    def set_password(self, username: str, password: str):
        """
        Set user password (hashed with bcrypt).
        
        Args:
            username: Username
            password: Plain text password
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.passwords[username] = hashed.decode('utf-8')
        self._save_users()
        logger.debug(f"Password set for user: {username}")
    
    def verify_password(self, username: str, password: str) -> bool:
        """
        Verify user password.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            True if password is correct
        """
        if username not in self.passwords:
            return False
        
        stored_hash = self.passwords[username].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        if not self.verify_password(username, password):
            logger.warning(f"Failed authentication attempt for: {username}")
            return None
        
        user = self.get_user_by_username(username)
        if user and user.enabled:
            user.last_login = datetime.utcnow().isoformat()
            self._save_users()
            logger.info(f"User authenticated: {username}")
            return user
        
        return None
    
    def get_user_permissions(self, user_id: str) -> List[str]:
        """
        Get user permissions based on role.
        
        Args:
            user_id: User ID
            
        Returns:
            List of permission strings
        """
        user = self.get_user(user_id)
        if not user:
            return []
        
        # In production, load from config
        from backend.config_manager import get_config
        config = get_config()
        
        role = config.get_role(user.role_id)
        if role:
            return role.get('permissions', [])
        
        return []
    
    def has_permission(self, user_id: str, permission: str) -> bool:
        """
        Check if user has specific permission.
        
        Args:
            user_id: User ID
            permission: Permission string
            
        Returns:
            True if user has permission
        """
        permissions = self.get_user_permissions(user_id)
        return permission in permissions
