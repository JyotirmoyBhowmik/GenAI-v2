# GenAI Platform

Enterprise-grade GenAI orchestration platform with multi-division architecture, knowledge graph, and comprehensive connectors.

## 🌟 Features

### Multi-Division Architecture
- **3-Level Hierarchy**: Division → Department → User
- **Complete Data Isolation**: Division, department, and user-level segregation
- **Built-in Divisions**: FMCG, Manufacturing, Hotel, Stationery, Retail, Corporate

### AI Models (12+)
- **Cloud Models**: OpenAI GPT, Google Gemini, Anthropic Claude, Grok
- **Local Models**: Llama 3, Mistral, Mixtral (via Ollama)
- **Specialized Models**: SBERT, PII Classifier, OCR, Market Intelligence

### Comprehensive Connectors
- **ERP**: SAP, Oracle, Tally, Zoho Books
- **CRM**: Salesforce, Zoho CRM, Freshdesk
- **HRMS**: DarwinBox, Keka, BambooHR
- **DMS**: SharePoint Online, OneDrive, Google Drive
- **Email**: Outlook 365, Gmail
- **Files**: Excel, PDF, Word, CSV, Images, Folders

### Knowledge Graph
- Entity linking across all data sources
- Graph-based RAG routing
- Relationship mapping
- Smart recommendations

### Enterprise Security
- **RBAC**: 6 predefined roles
- **ABAC**: Attribute-based access control
- **PII Detection**: Automatic redaction
- **Data Masking**: Dynamic response filtering
- **Encryption**: At-rest and in-transit

### Persona System
9+ built-in personas:
- HR Assistant
- Finance Analyst
- Sales Coach
- MIS Automation Bot
- Market Intelligence Bot
- Excel Expert
- Email Writing Bot
- IT Troubleshooter
- And more...

### Governance & Compliance
- Retention policies
- Audit trails
- Compliance reporting
- Policy violation detection
- Consent management

### Billing & Monitoring
- User/Department/Division-level cost tracking
- Token usage monitoring
- Automated invoice generation
- Cost optimization suggestions

### Plugin System
- Custom connectors
- Custom personas
- Division-specific tools
- Marketplace support

## 🚀 Quick Start

### Prerequisites
- Python 3.14 or higher
  > **Note**: Python 3.14 is experimental. Many packages (like `numpy`) may not have pre-built wheels, requiring **Microsoft Visual C++ 14.0 or greater** to build from source.
- Ollama (for local models) - optional
- Tesseract OCR - optional for PDF OCR

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/example/genai_platform.git
cd genai_platform
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.template .env
# Edit .env with your API keys and settings
```

5. **Initialize the platform**
```bash
python scripts/initialize.py
```

6. **Launch the GUI**
```bash
python gui/main_window.py
# Or use the installed command:
genai-platform
```

## 📖 Usage

### Launching the Application

**Desktop GUI**:
```bash
genai-platform
```

**CLI Mode**:
```bash
genai-cli --help
```

**API Server**:
```bash
genai-server --host 0.0.0.0 --port 8000
```

### Basic Workflow

1. **Select Division & Department**: Choose from the left panel
2. **Choose Persona**: Select AI behavior (HR Assistant, Finance Analyst, etc.)
3. **Select Model**: Pick from 12+ AI models
4. **Ingest Data**: Upload files, connect to ERP/CRM/HRMS, or link SharePoint
5. **Query**: Ask questions, analyze data, generate reports
6. **Review**: Check citations, audit trails, and billing stats

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              PyQt6 GUI Interface                │
├─────────────────────────────────────────────────┤
│           Orchestration Engine                  │
│        (RAG, Routing, Guardrails)              │
├─────────────────────────────────────────────────┤
│  Model Layer (12+ Models) │ Persona System      │
├─────────────────────────────────────────────────┤
│  Data Layer:                                    │
│  - Vector DB (Chroma)                          │
│  - Knowledge Graph (NetworkX)                  │
│  - SQL Warehouse (SQLite)                      │
├─────────────────────────────────────────────────┤
│  Application Connectors:                        │
│  ERP │ CRM │ HRMS │ DMS │ Email │ Files        │
├─────────────────────────────────────────────────┤
│  Infrastructure:                                │
│  MDM │ Security │ Governance │ Billing │ Backup│
└─────────────────────────────────────────────────┘
```

## 🔒 Security

- **RBAC**: Role-based access control with 6 levels
- **ABAC**: Attribute-based policies (division, department, location, etc.)
- **PII Detection**: Automatic detection and redaction
- **Encryption**: AES-256 for data at rest
- **Audit Logs**: Complete activity tracking
- **Data Isolation**: Division and department-level separation

## 📊 Sample Data

Included sample datasets:
- **FMCG**: Sales data, distribution, POS, promotions
- **Manufacturing**: Production logs, BOM, QC documents
- **Hotel**: Bookings, guest data, sales reports
- **Stationery**: Catalogs, vendor price lists
- **Shared**: HR policies, finance reports, market research

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ -v --cov=backend --cov=gui --cov-report=html
```

## 📚 Documentation

- [User Manual](docs/USER_MANUAL.md)
- [Administrator Guide](docs/ADMIN_GUIDE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Plugin Development](docs/PLUGIN_DEVELOPMENT.md)

## 🔌 Plugin Development

Create custom plugins:
```python
from backend.plugins.plugin_framework import BasePlugin

class MyCustomPlugin(BasePlugin):
    def execute(self, context):
        # Your plugin logic
        pass
```

See [Plugin Development Guide](docs/PLUGIN_DEVELOPMENT.md) for details.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/example/genai_platform/issues)
- Email: support@genai.example.com

## 🎯 Roadmap

- [ ] Additional cloud model integrations
- [ ] More enterprise connectors (Workday, ServiceNow)
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

## ⚙️ Configuration

Key configuration files:
- `.env` - Environment variables and API keys
- `config/app_config.yaml` - Application settings
- `config/divisions.yaml` - Division and department setup
- `config/models.yaml` - Model catalog and costs
- `config/personas.yaml` - Persona definitions
- `config/policies.yaml` - Security and compliance policies

## 🔄 Backup & Recovery

Automatic backups include:
- Vector database snapshots
- Knowledge graph exports
- SQL warehouse dumps
- Configuration backups

Restore using:
```bash
python scripts/restore.py --backup-id <backup_id>
```

## 📈 Monitoring

Access monitoring dashboards:
- **Billing Stats**: View costs by user/department/division
- **Audit Logs**: Track all system activities
- **Compliance Dashboard**: Monitor policy adherence
- **Performance Metrics**: System health and usage

---

**Built with ❤️ for Enterprise AI**
