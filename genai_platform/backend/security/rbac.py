"""
GenAI Platform - RBAC Manager
Role-Based Access Control implementation
"""

from typing import List, Dict, Any, Optional
from loguru import logger


class RBACManager:
    """
    Role-Based Access Control manager.
    Enforces permissions based on user roles.
    """
    
    def __init__(self):
        """Initialize RBAC manager."""
        from backend.config_manager import get_config
        self.config = get_config()
        
        self.roles = self._load_roles()
        logger.info(f"RBAC Manager initialized with {len(self.roles)} roles")
    
    def _load_roles(self) -> Dict[str, Dict[str, Any]]:
        """Load roles from configuration."""
        roles_list = self.config.get('policies', 'roles', default=[])
        
        roles_dict = {}
        for role in roles_list:
            role_id = role.get('id')
            if role_id:
                roles_dict[role_id] = role
        
        return roles_dict
    
    def get_role(self, role_id: str) -> Optional[Dict[str, Any]]:
        """
        Get role by ID.
        
        Args:
            role_id: Role identifier
            
        Returns:
            Role configuration dict or None
        """
        return self.roles.get(role_id)
    
    def get_permissions(self, role_id: str) -> List[str]:
        """
        Get permissions for a role.
        
        Args:
            role_id: Role identifier
            
        Returns:
            List of permission strings
        """
        role = self.get_role(role_id)
        if role:
            return role.get('permissions', [])
        return []
    
    def has_permission(self, role_id: str, permission: str) -> bool:
        """
        Check if role has a specific permission.
        
        Args:
            role_id: Role identifier
            permission: Permission string
            
        Returns:
            True if role has permission
        """
        permissions = self.get_permissions(role_id)
        return permission in permissions
    
    def can_access_division(self, role_id: str, division_id: str, user_division: str) -> bool:
        """
        Check if user can access a division.
        
        Args:
            role_id: User's role
            division_id: Division to access
            user_division: User's own division
            
        Returns:
            True if access allowed
        """
        # Super admin can access all divisions
        if role_id == 'super_admin':
            return True
        
        # Others can only access their own division
        return division_id == user_division
    
    def can_access_department(
        self,
        role_id: str,
        department_id: str,
        user_department: str,
        user_division: str,
        target_division: str
    ) -> bool:
        """
        Check if user can access a department.
        
        Args:
            role_id: User's role
            department_id: Department to access
            user_department: User's own department
            user_division: User's division
            target_division: Target division
            
        Returns:
            True if access allowed
        """
        # Must be same division first
        if user_division != target_division:
            return self.can_access_division(role_id, target_division, user_division)
        
        # Super admin and division admin can access all departments in division
        if role_id in ['super_admin', 'division_admin']:
            return True
        
        # Department admin can access their department
        if role_id == 'department_admin':
            return department_id == user_department
        
        # Others can only access their own department
        return department_id == user_department
    
    def can_ingest_data(self, role_id: str) -> bool:
        """Check if role can ingest data."""
        return self.has_permission(role_id, 'ingest_files') or \
               self.has_permission(role_id, 'access_connectors')
    
    def can_view_audit_logs(self, role_id: str) -> bool:
        """Check if role can view audit logs."""
        return self.has_permission(role_id, 'view_audit_logs') or \
               self.has_permission(role_id, 'view_division_audit_logs') or \
               self.has_permission(role_id, 'view_department_audit_logs')
    
    def can_manage_users(self, role_id: str) -> bool:
        """Check if role can manage users."""
        return self.has_permission(role_id, 'manage_users') or \
               self.has_permission(role_id, 'manage_division_users') or \
               self.has_permission(role_id, 'manage_department_users')
