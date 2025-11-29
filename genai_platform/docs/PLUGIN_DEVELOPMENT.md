"""
GenAI Platform - Plugin Development Guide

## Overview
The GenAI Platform supports custom plugins for extending functionality with connectors, personas, and tools.

## Plugin Types

### 1. Connector Plugins
Connect to custom data sources.

```python
from backend.plugins.plugin_framework import ConnectorPlugin
from typing import Dict, List, Any, Optional

class MyCustomConnector(ConnectorPlugin):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key')
    
    def connect(self) -> bool:
        # Implement connection logic
        return True
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        # Fetch data from your source
        return [{'id': '1', 'data': 'example'}]
    
    def execute(self, context: Dict[str, Any]) -> Any:
        return self.fetch_data()
```

### 2. Persona Plugins
Create custom AI personas.

```python
from backend.plugins.plugin_framework import PersonaPlugin

class MyCustomPersona(PersonaPlugin):
    def get_system_prompt(self) -> str:
        return "You are a specialized assistant for..."
    
    def get_allowed_models(self) -> List[str]:
        return ['gpt-4', 'claude-3-opus']
    
    def execute(self, context: Dict[str, Any]) -> Any:
        return {
            'prompt': self.get_system_prompt(),
            'models': self.get_allowed_models()
        }
```

### 3. Tool Plugins
Add custom tools and capabilities.

```python
from backend.plugins.plugin_framework import ToolPlugin

class MyDataAnalyzer(ToolPlugin):
    def run(self, inputs: Dict[str, Any]) -> Any:
        data = inputs.get('data', [])
        # Perform analysis
        return {
            'records': len(data),
            'analysis': 'Complete'
        }
    
    def execute(self, context: Dict[str, Any]) -> Any:
        return self.run(context)
```

## Plugin Structure

Place your plugin in:
```
backend/plugins/custom/my_plugin.py
```

Each plugin file should:
1. Define a class inheriting from BasePlugin, ConnectorPlugin, PersonaPlugin, or ToolPlugin
2. Implement required abstract methods
3. Include metadata in config

## Plugin Configuration

Create a config dict:
```python
config = {
    'name': 'My Custom Plugin',
    'version': '1.0.0',
    'enabled': True,
    'author': 'Your Name',
    'description': 'Plugin description',
    # Plugin-specific settings
}
```

## Loading Plugins

### Automatic Loading
```python
from backend.plugins.plugin_framework import PluginLoader

loader = PluginLoader()
loader.load_all_plugins()
```

### Manual Loading
```python
loader = PluginLoader()
plugin = loader.load_plugin('path/to/my_plugin.py')
```

## Plugin Registry

Register plugins centrally:
```python
from backend.plugins.plugin_framework import PluginRegistry

registry = PluginRegistry()
registry.register_plugin(
    plugin_id='my_custom_plugin',
    plugin_type='connector',
    plugin_class=MyCustomConnector,
    metadata={'version': '1.0.0'}
)

# Get plugins by type
connectors = registry.get_plugins_by_type('connector')
```

## Best Practices

1. **Error Handling**: Always wrap operations in try-except
2. **Logging**: Use loguru logger for debugging
3. **Configuration**: Accept config dict in __init__
4. **Testing**: Write unit tests for your plugin
5. **Documentation**: Add docstrings to all methods
6. **Versioning**: Use semantic versioning

## Example: Complete Plugin

```python
from backend.plugins.plugin_framework import ConnectorPlugin
from typing import Dict, List, Any, Optional
from loguru import logger

class CustomAPIConnector(ConnectorPlugin):
    \"\"\"Connects to a custom REST API.\"\"\"
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_url = config.get('api_url')
        self.api_key = config.get('api_key')
    
    def connect(self) -> bool:
        try:
            # Test API connection
            import requests
            response = requests.get(
                f"{self.api_url}/health",
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    def fetch_data(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        try:
            import requests
            response = requests.get(
                f"{self.api_url}/data",
                headers={'Authorization': f'Bearer {self.api_key}'},
                params=query or {}
            )
            return response.json().get('data', [])
        except Exception as e:
            logger.error(f"Fetch failed: {e}")
            return []
    
    def execute(self, context: Dict[str, Any]) -> Any:
        return self.fetch_data(context.get('query'))
```

## Distribution

1. Package your plugin as a Python file
2. Include documentation and examples
3. Specify dependencies in comments
4. Test with the platform
5. Share via GitHub or internal repository

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review existing plugin examples
- Consult platform documentation
