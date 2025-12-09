<!-- GitHub Copilot assistant instructions for contributors and AI agents -->
# GenAI Platform — Copilot Instructions

This document helps AI coding assistants (Copilot, other agents) be productive in the GenAI Platform codebase.
It focuses on predictable conventions and examples. Avoid speculative or aspirational items — document what exists.

## Quick architecture summary
- Single monorepo Python application with a PyQt6 GUI and modular backend.
- Core layers:
  - GUI: `gui/` (PyQt6 desktop app)
  - Orchestration: `backend/orchestration/query_processor.py` (main query flow)
  - Model layer: `backend/models/` (adapters, router, dummy fallback)
  - Data layer: `backend/data/` (vector store, knowledge graph, SQL warehouse)
  - Connectors: `backend/connectors/*` (ERP, CRM, DMS, email, file connectors)
  - MDM, Security, Governance, Billing: `backend/mdm/`, `backend/security/`, `backend/billing/`

## Top-level patterns & conventions
- Config-driven: Nearly everything (models, personas, roles, policies, division structure) is YAML under `config/` and accessed through `backend/config_manager.py` using the `get_config()` singleton.
- Division isolation: `division_id`/`department_id` are used to partition data — vector collections use naming `genai_platform_{division_id}`, and record metadata often adds `_division_id` and `_department_id`.
- Plugin system: Write plugins using `backend/plugins/plugin_framework.BasePlugin`. Plugins live in `backend/plugins/custom` and are loaded by `PluginLoader`.
- Connectors follow `BaseConnector` interface: `connect()`, `disconnect()`, `test_connection()`, `fetch_data()`, `get_schema()`.
- Model adapters: Extend `backend/models/base_model.BaseModelAdapter`. Implement `generate()` and `stream_generate()` and plug in using the providers map in `backend/models/model_router.py`.
- PII and RBAC are config-driven and found under `backend/security/`. PII patterns and redaction behaviors come from `config/policies.yaml`.

## Examples (copyable snippets)
- Add a new model adapter skeleton:
```python
from backend.models.base_model import BaseModelAdapter, ModelResponse

class MyAdapter(BaseModelAdapter):
    def generate(self, prompt, max_tokens=None, temperature=0.7, **kwargs) -> ModelResponse:
        # Implement API call here
        return ModelResponse(text='...', model_id=self.model_id, provider=self.provider, tokens_used=0, cost=0.0, metadata={})

    def stream_generate(self, prompt, **kwargs):
        yield '...'  # stream text
```
Add to router mapping in `model_router.py` under the provider case and add `provider` entry to `config/models.yaml`.

- Add a connector scaffold by extending `BaseConnector` in `backend/connectors/` and place it in a subfolder (e.g., `backend/connectors/crm`).

## Developer workflows
- Setup:
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env  # then edit API keys
```
- Initialize environment (**will create DBs and directories**):
```bash
python scripts/initialize.py
```
- Run GUI (desktop):
```bash
python gui/main_window.py
```
- Run tests:
```bash
pytest tests/ -v
pytest tests/ -v --cov=backend --cov=gui --cov-report=html
```

## Common gotchas & project-specific notes
- Many adapters/optional features are optional and fall back to mocks (e.g., `DummyModelAdapter`, mock connectors, mock embeddings) if the optional dependencies or API keys are not installed or present. Check `Dockerfile`, `.env.template`, and `config/models.yaml`.
- Vector DB uses Chroma (`chromadb`) with persistence under `data/chroma_db`. Collections follow `genai_platform_{division_id}` naming convention.
- Embedding generation optionally uses `sentence-transformers`. If missing, `EmbeddingGenerator` falls back to mock embeddings.
- `PIIDetector` uses regex-driven detection. Patterns and redaction methods are defined in `config/policies.yaml`. Avoid introducing new detection methods without updating the policies YAML.
- Use `get_config()` (from `backend/config_manager.py`) to access YAML config. Do not read YAML directly from files scattered across code; this keeps runtime state consistent.

## Testing & mocks
- Tests rely heavily on `MockConnector`, `DummyModelAdapter`, and `Mocking` across modules; follow existing tests for patterns. Tests are under `tests/` and use `unittest`/`pytest` conventions.
- When adding mocking utilities, follow the `Base*` abstract interfaces and register minimal metadata for compatibility.

## Adding features & PR advice for AI agents
- Focus on config consistency: add config entries in `config/models.yaml` or `config/personas.yaml` and wire them via `backend/config_manager.py`.
- Where possible, ensure code honors division/department isolation by copying metadata patterns (`_division_id`, `_department_id`) and using `get_config().get_division()` lookups.
- Add tests for new modules that illustrate intended operational modes — mocked and integrated (if optional external deps exist).
- Use existing logging standards (loguru) at INFO/DEBUG level.

## Files to inspect first when working on a change
- `backend/config_manager.py` — central configuration contract and `get_config()` API
- `backend/orchestration/query_processor.py` — main flow tying together RBAC, PII, model routing
- `backend/models/model_router.py` — choose and route models; shows how to wire adapters
- `backend/models/base_model.py` — model adapter interface & dummy fallback
- `backend/plugins/plugin_framework.py` — plugin contract and PluginLoader
- `backend/ingestion/` — ingestion pipeline and vector/knowledge graph integration
- `config/*.yaml` — authoritative config for models, personas, policies

If anything looks unclear or you need deeper guidance on a specific feature (models, connectors, plugin extension, or test structure), please mention it — I'll refine these instructions with code-level examples or file edits.

---
Last updated: `README.md` & code inspected — add specific file references in PRs where you make non-trivial changes.
