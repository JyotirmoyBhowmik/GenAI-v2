# GenAI Platform - Quick Reference Guide

## 🚀 Quick Start

### 1. Setup & Installation
```bash
# Run automated setup
setup.bat

# Or manually:
pip install -r requirements.txt
python scripts/initialize.py
```

### 2. Launch Platform
```bash
python gui/main_window.py
# Or: genai-platform
```

### 3. Default Login
- **Username**: `admin`
- **Password**: `Admin@123`

---

## 📁 Project Structure

```
genai_platform/
├── backend/           # Core backend modules
│   ├── config_manager.py
│   ├── mdm/          # User, division, department management
│   ├── security/     # RBAC, ABAC, PII detection
│   ├── models/       # Model adapters & routing
│   ├── orchestration/  # Query processing
│   ├── connectors/   # ERP, CRM, HRMS, Files
│   ├── ingestion/    # Data ingestion
│   ├── billing/      # Cost tracking
│   ├── backup/       # Backup & restore
│   └── plugins/      # Plugin framework
├── gui/              # PyQt6 desktop interface
│   ├── main_window.py
│   └── panels/       # Left, center, bottom panels
├── config/           # YAML configurations
│   ├── app_config.yaml
│   ├── divisions.yaml
│   ├── models.yaml
│   ├── personas.yaml
│   └── policies.yaml
├── scripts/          # Utility scripts
├── tests/            # Test suite
└── data/             # Persisted data
```

---

## 🔧 Common Operations

### Generate Sample Data
```bash
python scripts/generate_sample_data.py
```

### Create Backup
```bash
backup.bat
# Or: python -m backend.backup.backup_manager
```

### Run Tests
```bash
python scripts/run_tests.py
```

### Check System Status
```bash
python scripts/initialize.py
```

---

## 🎯 Key Features

### 1. Multi-Division Architecture
- 6 divisions: FMCG, Manufacturing, Hotel, Stationery, Retail, Corporate
- 23 departments with strict data isolation
- Division-level vector DB namespacing

### 2. Security & Compliance
- **RBAC**: 6 roles (Super Admin, Division Admin, Department Admin, Analyst, Viewer, Approver)
- **ABAC**: Division/department/sensitivity-based access
- **PII Detection**: Email, phone, SSN, credit cards, Aadhaar, PAN
- **Redaction**: 3 methods (mask_all, mask_partial, mask_middle)

### 3. AI Models (12+)
- **Cloud**: GPT-4, GPT-3.5, Gemini Pro/Ultra, Claude 3, Grok
- **Local**: Llama 3, Mistral, Mixtral (via Ollama)
- **Special**: SBERT, PII Classifier, OCR

### 4. Personas (9)
- HR Assistant, Finance Analyst, Sales Coach
- MIS Bot, Market Intel Bot, Excel Expert
- Email Writer, IT Troubleshooter, General Assistant

### 5. Connectors
- **ERP**: SAP, Oracle, Tally, Zoho Books
- **CRM**: Salesforce, Zoho CRM, Freshdesk
- **HRMS**: DarwinBox, Keka, BambooHR
- **Files**: Excel, CSV, PDF

---

## ⚙️ Configuration

### API Keys (.env file)
```env
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GROK_API_KEY=your_key_here
```

### Modify Divisions
Edit `config/divisions.yaml` to add/modify divisions and departments.

### Add Models
Edit `config/models.yaml` to configure model catalog.

### Create Personas
Edit `config/personas.yaml` to define custom personas.

---

##  💰 Billing & Cost Tracking

```python
from backend.billing.billing_engine import CostTracker, BillingEngine

# Track costs
tracker = CostTracker()
tracker.record_cost(user_id, division_id, department_id, model_id, tokens, cost)

# Generate reports
engine = BillingEngine(tracker)
report = engine.generate_user_report(user_id, month='2024-01')
```

---

## 🔌 Plugin Development

Create custom plugins by extending base classes:

```python
from backend.plugins.plugin_framework import ToolPlugin

class MyCustomPlugin(ToolPlugin):
    def execute(self, context):
        # Your plugin logic
        return result
    
    def run(self, inputs):
        return self.execute(inputs)
```

---

## 🧪 Testing

Run tests:
```bash
python scripts/run_tests.py
# Or: python -m unittest discover tests
```

Test coverage:
- Config management
- User authentication
- RBAC/ABAC
- PII detection
- Connectors
- Model routing
- Query processing
- Billing

---

## 🆘 Troubleshooting

### Import Errors
Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

### Database Not Found
Run initialization:
```bash
python scripts/initialize.py
```

### No API Keys
Platform works without API keys using DummyModelAdapter for testing.

### GUI Won't Launch
Check PyQt6 installation:
```bash
pip install PyQt6
```

---

## 📚 Documentation

- **README.md**: Full documentation
- **Implementation Plan**: `C:\Users\TEST\.gemini\antigravity\brain\[id]\implementation_plan.md`
- **Walkthrough**: `C:\Users\TEST\.gemini\antigravity\brain\[id]\walkthrough.md`

---

## 🔄 Version

**GenAI Platform v1.0.0**

---

For support or questions, refer to the main README.md file.
