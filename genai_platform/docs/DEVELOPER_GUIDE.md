# GenAI Platform - Developer Guide

## Architecture Overview

```
┌─────────────────────────────────┐
│   PyQt6 GUI / REST API          │
├─────────────────────────────────┤
│   Orchestration Engine          │
│   (Query Processor)             │
├─────────────────────────────────┤
│   Model Layer / Connectors      │
│   (Model Router, Adapters)      │
├─────────────────────────────────┤
│   Data Layer                    │
│   (Vector DB, Knowledge Graph)  │
├─────────────────────────────────┤
│   Infrastructure                │
│   (Security, Billing, Backup)   │
└─────────────────────────────────┘
```

## Development Setup

```bash
# Clone and setup
git clone <repo>
cd genai_platform

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Initialize
python scripts/initialize.py

# Run tests
pytest tests/ -v --cov=backend
```

## Project Structure

```
genai_platform/
├── backend/              # Core backend modules
│   ├── models/          # AI model adapters
│   ├── connectors/      # Data source connectors
│   ├── data/            # Data layer (vector DB, graphs)
│   ├── security/        # RBAC, PII detection, encryption
│   ├── ingestion/       # Data ingestion pipeline
│   ├── orchestration/   # Query processing engine
│   └── plugins/         # Plugin system
├── gui/                 # PyQt6 GUI application
├── scripts/             # Utility scripts
├── config/              # YAML configuration files
├── tests/               # Unit & integration tests
└── docs/                # Documentation
```

## Key Components

### 1. Configuration Manager
Centralized config access via `get_config()`:
```python
from backend.config_manager import get_config

config = get_config()
division = config.get_division('fmcg')
models = config.list_models()
```

### 2. Model Router
Routes queries to appropriate models:
```python
from backend.models.model_router import ModelRouter

router = ModelRouter()
response = router.route(
    prompt="Your question",
    model_id="gpt-4",
    persona_id="sales_coach"
)
```

### 3. Query Processor
Main orchestration engine:
```python
from backend.orchestration.query_processor import QueryProcessor, QueryContext

processor = QueryProcessor()
context = QueryContext(
    user_id="user1",
    division_id="fmcg",
    department_id="sales",
    persona_id="sales_coach"
)
response = processor.process("Your query", context)
```

### 4. Plugin System
Extend with custom plugins:
```python
from backend.plugins.plugin_framework import BasePlugin

class MyPlugin(BasePlugin):
    def execute(self, context):
        # Your logic here
        return result
```

### 5. Connectors
Create custom connectors:
```python
from backend.connectors.base_connector import BaseConnector

class MyConnector(BaseConnector):
    def connect(self):
        # Connect to data source
        pass
    
    def fetch_data(self, query=None):
        # Fetch data
        return data
```

## Adding a Feature

### 1. Add Model Adapter
```python
# backend/models/custom_adapter.py
from backend.models.base_model import BaseModelAdapter, ModelResponse

class CustomAdapter(BaseModelAdapter):
    def generate(self, prompt, **kwargs):
        # Call your model API
        return ModelResponse(
            text="response",
            model_id=self.model_id,
            provider="custom",
            tokens_used=100,
            cost=0.01,
            metadata={}
        )
```

### 2. Register in Model Router
Edit `backend/models/model_router.py`:
```python
elif provider == 'custom':
    from backend.models.custom_adapter import CustomAdapter
    adapter = CustomAdapter(model_config)
```

### 3. Add Config Entry
Edit `config/models.yaml`:
```yaml
- id: "custom-model"
  provider: "custom"
  model_name: "custom-model"
  enabled: true
```

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_core.py::TestConfigManager -v
```

### Generate Coverage Report
```bash
pytest tests/ --cov=backend --cov-report=html
```

### Mock Objects
```python
from backend.connectors.base_connector import MockConnector
from backend.models.base_model import DummyModelAdapter

# Use in tests for isolated testing
```

## Code Style

- Follow PEP 8
- Use type hints
- Document with docstrings
- Format with `black`: `black backend/`
- Lint with `flake8`: `flake8 backend/`

## Common Patterns

### Configuration Access
```python
from backend.config_manager import get_config
config = get_config()
value = config.get('app', 'logging', 'level')
```

### Division Isolation
```python
# Always add division context
metadata['_division_id'] = division_id
metadata['_department_id'] = department_id
```

### Logging
```python
from loguru import logger
logger.info("Message")
logger.error("Error occurred")
```

### Error Handling
```python
try:
    # Your code
except SpecificException as e:
    logger.error(f"Error: {e}")
    raise
```

## Documentation

- Update docstrings for new functions
- Keep README.md current
- Add API documentation in code
- Document breaking changes

## Deployment

### Docker Build
```bash
docker build -t genai-platform:latest .
```

### Docker Run
```bash
docker-compose up -d
```

### Environment Variables
See `.env.template` for all configurable settings.

---
**Version**: 1.0.0
**Last Updated**: December 2024
