"""
GenAI Platform - Configuration Manager
Handles loading and management of all configuration files
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger
from dotenv import load_dotenv


class ConfigManager:
    """
    Central configuration management system.
    Loads and provides access to all YAML configurations and environment variables.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Path to configuration directory. If None, uses default.
        """
        # Load environment variables
        load_dotenv()
        
        # Determine config directory
        if config_dir is None:
            # Get project root (assuming we're in backend/config/)
            project_root = Path(__file__).parent.parent.parent
            config_dir = project_root / "config"
        
        self.config_dir = Path(config_dir)
        
        #Load all configurations
        self._configs: Dict[str, Any] = {}
        self._load_all_configs()
        
        logger.info(f"Configuration loaded from {self.config_dir}")
    
    def _load_all_configs(self):
        """Load all YAML configuration files."""
        config_files = {
            'app': 'app_config.yaml',
            'divisions': 'divisions.yaml',
            'models': 'models.yaml',
            'personas': 'personas.yaml',
            'policies': 'policies.yaml'
        }
        
        for config_name, filename in config_files.items():
            filepath = self.config_dir / filename
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self._configs[config_name] = yaml.safe_load(f)
                logger.debug(f"Loaded {config_name} configuration from {filename}")
            except FileNotFoundError:
                logger.warning(f"Configuration file not found: {filepath}")
                self._configs[config_name] = {}
            except yaml.YAMLError as e:
                logger.error(f"Error parsing {filename}: {e}")
                self._configs[config_name] = {}
    
    def get(self, config_type: str, *keys, default=None) -> Any:
        """
        Get configuration value.
        
        Args:
            config_type: Type of config ('app', 'divisions', 'models', 'personas', 'policies')
            *keys: Nested keys to traverse
            default: Default value if key not found
            
        Returns:
            Configuration value
            
        Example:
            config.get('app', 'logging', 'level')  # Returns 'INFO'
            config.get('models', 'models', 0, 'name')  # Returns first model name
        """
        config = self._configs.get(config_type, {})
        
        for key in keys:
            if isinstance(config, dict):
                config = config.get(key, default)
            elif isinstance(config, list) and isinstance(key, int):
                try:
                    config = config[key]
                except IndexError:
                    return default
            else:
                return default
        
        return config if config is not None else default
    
    def get_env(self, key: str, default: str = "") -> str:
        """
        Get environment variable.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value
        """
        return os.getenv(key, default)
    
    def get_env_bool(self, key: str, default: bool = False) -> bool:
        """Get environment variable as boolean."""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_env_int(self, key: str, default: int = 0) -> int:
        """Get environment variable as integer."""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default
    
    def reload(self):
        """Reload all configurations from disk."""
        self._load_all_configs()
        logger.info("Configuration reloaded")
    
    def get_division(self, division_id: str) -> Optional[Dict[str, Any]]:
        """
        Get division configuration by ID.
        
        Args:
            division_id: Division identifier (e.g., 'fmcg', 'manufacturing')
            
        Returns:
            Division configuration dict or None
        """
        divisions = self.get('divisions', 'divisions', default=[])
        for division in divisions:
            if division.get('id') == division_id:
                return division
        return None
    
    def get_department(self, division_id: str, department_id: str) -> Optional[Dict[str, Any]]:
        """
        Get department configuration.
        
        Args:
            division_id: Division identifier
            department_id: Department identifier
            
        Returns:
            Department configuration dict or None
        """
        division = self.get_division(division_id)
        if not division:
            return None
        
        departments = division.get('departments', [])
        for dept in departments:
            if dept.get('id') == department_id:
                return dept
        return None
    
    def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get model configuration by ID.
        
        Args:
            model_id: Model identifier (e.g., 'gpt-4', 'llama3')
            
        Returns:
            Model configuration dict or None
        """
        models = self.get('models', 'models', default=[])
        for model in models:
            if model.get('id') == model_id:
                return model
        return None
    
    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """
        Get persona configuration by ID.
        
        Args:
            persona_id: Persona identifier (e.g., 'hr_assistant')
            
        Returns:
            Persona configuration dict or None
        """
        personas = self.get('personas', 'personas', default=[])
        for persona in personas:
            if persona.get('id') == persona_id:
                return persona
        return None
    
    def get_role(self, role_id: str) -> Optional[Dict[str, Any]]:
        """
        Get role configuration by ID.
        
        Args:
            role_id: Role identifier (e.g., 'super_admin', 'analyst')
            
        Returns:
            Role configuration dict or None
        """
        roles = self.get('policies', 'roles', default=[])
        for role in roles:
            if role.get('id') == role_id:
                return role
        return None
    
    def list_divisions(self) -> list:
        """Get list of all divisions."""
        return self.get('divisions', 'divisions', default=[])
    
    def list_models(self, enabled_only: bool = True) -> list:
        """Get list of all models."""
        models = self.get('models', 'models', default=[])
        if enabled_only:
            return [m for m in models if m.get('enabled', False)]
        return models
    
    def list_personas(self, enabled_only: bool = True) -> list:
        """Get list of all personas."""
        personas = self.get('personas', 'personas', default=[])
        if enabled_only:
            return [p for p in personas if p.get('enabled', False)]
        return personas
    
    def list_roles(self) -> list:
        """Get list of all roles."""
        return self.get('policies', 'roles', default=[])


# Global configuration instance
_config_instance: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """
    Get global configuration instance (singleton pattern).
    
    Returns:
        ConfigManager instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance


def reload_config():
    """Reload global configuration."""
    global _config_instance
    if _config_instance is not None:
        _config_instance.reload()
    else:
        _config_instance = ConfigManager()
