"""
GenAI Platform - Plugin Framework
Enables custom plugins for connectors, personas, and tools
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path
import importlib.util
from loguru import logger


class BasePlugin(ABC):
    """Abstract base class for all plugins."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize plugin.
        
        Args:
            config: Plugin configuration
        """
        self.config = config
        self.plugin_name = config.get('name', self.__class__.__name__)
        self.plugin_version = config.get('version', '1.0.0')
        self.enabled = config.get('enabled', True)
        
        logger.debug(f"Initialized plugin: {self.plugin_name} v{self.plugin_version}")
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """
        Execute plugin functionality.
        
        Args:
            context: Execution context
            
        Returns:
            Plugin result
        """
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get plugin metadata."""
        return {
            'name': self.plugin_name,
            'version': self.plugin_version,
            'enabled': self.enabled,
            'type': self.__class__.__name__
        }


class ConnectorPlugin(BasePlugin):
    """Base class for connector plugins."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection."""
        pass
    
    @abstractmethod
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch data from source."""
        pass


class PersonaPlugin(BasePlugin):
    """Base class for persona plugins."""
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get persona system prompt."""
        pass
    
    @abstractmethod
    def get_allowed_models(self) -> List[str]:
        """Get allowed models for this persona."""
        pass


class ToolPlugin(BasePlugin):
    """Base class for tool plugins."""
    
    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> Any:
        """Run tool with inputs."""
        pass


class PluginLoader:
    """Loads and manages plugins."""
    
    def __init__(self, plugins_dir: str = "./backend/plugins/custom"):
        """
        Initialize plugin loader.
        
        Args:
            plugins_dir: Directory containing plugin files
        """
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        
        self.loaded_plugins: Dict[str, BasePlugin] = {}
        
        logger.info(f"PluginLoader initialized (dir: {self.plugins_dir})")
    
    def load_plugin(self, plugin_path: str) -> Optional[BasePlugin]:
        """
        Load a plugin from file.
        
        Args:
            plugin_path: Path to plugin Python file
            
        Returns:
            Loaded plugin instance or None
        """
        try:
            # Load module dynamically
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin class (should be named Plugin or inherit from BasePlugin)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr != BasePlugin:
                    # Instantiate plugin
                    plugin = attr(config={})
                    self.loaded_plugins[plugin.plugin_name] = plugin
                    logger.info(f"Loaded plugin: {plugin.plugin_name}")
                    return plugin
            
            logger.warning(f"No plugin class found in {plugin_path}")
            return None
            
        except Exception as e:
            logger.error(f"Error loading plugin from {plugin_path}: {e}")
            return None
    
    def load_all_plugins(self):
        """Load all plugins from plugins directory."""
        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {self.plugins_dir}")
            return
        
        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            
            self.load_plugin(str(plugin_file))
        
        logger.info(f"Loaded {len(self.loaded_plugins)} plugins")
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """Get loaded plugin by name."""
        return self.loaded_plugins.get(plugin_name)
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins."""
        return [plugin.get_metadata() for plugin in self.loaded_plugins.values()]


class PluginRegistry:
    """Central registry for managing plugins."""
    
    def __init__(self):
        """Initialize plugin registry."""
        self.plugins: Dict[str, Dict[str, Any]] = {}
        logger.info("PluginRegistry initialized")
    
    def register_plugin(
        self,
        plugin_id: str,
        plugin_type: str,
        plugin_class: type,
        metadata: Dict[str, Any]
    ):
        """
        Register a plugin.
        
        Args:
            plugin_id: Unique plugin ID
            plugin_type: Plugin type (connector, persona, tool)
            plugin_class: Plugin class
            metadata: Plugin metadata
        """
        self.plugins[plugin_id] = {
            'id': plugin_id,
            'type': plugin_type,
            'class': plugin_class,
            'metadata': metadata
        }
        
        logger.info(f"Registered plugin: {plugin_id} ({plugin_type})")
    
    def get_plugins_by_type(self, plugin_type: str) -> List[Dict[str, Any]]:
        """Get all plugins of a specific type."""
        return [
            p for p in self.plugins.values()
            if p.get('type') == plugin_type
        ]
    
    def get_plugin(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get plugin by ID."""
        return self.plugins.get(plugin_id)


# Example plugin
class ExampleDataAnalyzerPlugin(ToolPlugin):
    """Example tool plugin for data analysis."""
    
    def execute(self, context: Dict[str, Any]) -> Any:
        """Analyze data provided in context."""
        data = context.get('data', [])
        return {
            'record_count': len(data),
            'analysis': 'Example analysis complete'
        }
    
    def run(self, inputs: Dict[str, Any]) -> Any:
        """Run data analysis."""
        return self.execute(inputs)


__all__ = [
    'BasePlugin',
    'ConnectorPlugin',
    'PersonaPlugin',
    'ToolPlugin',
    'PluginLoader',
    'PluginRegistry',
    'ExampleDataAnalyzerPlugin'
]
