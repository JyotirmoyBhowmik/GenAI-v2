# GenAI Platform — User Manual

## Introduction

The GenAI Platform is an enterprise-grade artificial intelligence orchestration system designed to help teams across multiple divisions leverage AI capabilities for data analysis, process automation, and intelligent decision-making.

## Getting Started

### System Requirements
- Python 3.10 or higher
- 4GB RAM (8GB recommended)
- 2GB disk space for databases
- Internet connection for cloud AI models (OpenAI, Google, Anthropic)

### First-Time Setup

1. **Initialize the Platform**
   ```bash
   python scripts/initialize.py
   ```
   This creates all necessary directories, databases, and default users.

2. **Configure API Keys** (Optional)
   ```bash
   cp .env.template .env
   # Edit .env with your API keys for cloud models
   ```

3. **Launch the Application**
   ```bash
   python gui/main_window.py
   ```

### Default Credentials
- Username: `admin`
- Password: `Admin@123`

## Basic Usage

### 1. Selecting Your Division and Department
- Use the **Left Panel** to select your Division and Department
- Only divisions and departments your role has access to will be available

### 2. Choosing a Persona
- Personas define the AI's behavior and capabilities
- Available personas:
  - **HR Assistant** — HR queries, employee data, policies
  - **Finance Analyst** — Financial data analysis, budgets, forecasts
  - **Sales Coach** — Sales strategies, pipeline analysis, forecasting
  - **Market Intelligence Bot** — Market trends, competitive analysis
  - **Excel Expert** — Spreadsheet analysis and generation
  - **Email Writer** — Professional email composition
  - **IT Troubleshooter** — IT issues and solutions

### 3. Selecting a Model
- Choose from available AI models:
  - **Cloud Models**: GPT-4, Claude 3, Gemini (require API keys)
  - **Local Models**: Llama 3, Mistral (free, offline)
- Model choice affects response quality and cost

### 4. Submitting Your Query
- Type your question in the **Bottom Input Panel**
- Click **Send** or press Enter
- The AI will process your query and return a response

### 5. Understanding the Response
- Response includes:
  - AI-generated text
  - Model used and tokens consumed
  - Cost (if applicable)
  - Any personally identifiable information (PII) redacted for security

## Features

### Data Ingestion
- Upload Excel, CSV, or PDF files
- Connect to enterprise systems (ERP, CRM, HRMS)
- Automatic data validation and PII detection

### Knowledge Graph
- Automatic entity linking across data sources
- Relationship mapping for intelligent recommendations
- Graph-based retrieval for accurate citations

### Security & Compliance
- Role-based access control (6 predefined roles)
- Division and department-level data isolation
- Automatic PII redaction
- Comprehensive audit logging
- Compliance policy enforcement

### Billing & Cost Tracking
- Real-time cost tracking by user, department, and division
- Usage statistics and trends
- Invoice generation

## Advanced Features

### Custom Personas
Create custom personas tailored to your organization:
1. Edit `config/personas.yaml`
2. Define system prompt, allowed models, and capabilities
3. Restart the application

### Plugins
Extend functionality with custom plugins:
1. Create plugin in `backend/plugins/custom/`
2. Inherit from `BasePlugin` class
3. Platform automatically loads and registers

### Batch Processing
Generate data for multiple divisions:
```bash
genai-cli generate --division fmcg --count 1000
```

## Troubleshooting

### Application Won't Start
- Check Python version: `python --version` (need 3.10+)
- Install dependencies: `pip install -r requirements.txt`
- Initialize: `python scripts/initialize.py`

### Cloud Models Not Working
- Verify API keys in `.env`
- Test connection: `genai-cli health`
- Check internet connectivity

### Slow Performance
- Reduce batch size for ingestion
- Use local models (Llama, Mistral) instead of cloud
- Check available disk space and RAM

### PII Redaction Issues
- Redaction rules are configurable in `config/policies.yaml`
- Update patterns to detect additional PII types
- Test with: `genai-cli health`

## Support

- **Documentation**: See `docs/` directory
- **API Reference**: Run server and visit http://localhost:8000/api/docs
- **Issues**: Report bugs and request features via GitHub

## Security Notes

- Never commit `.env` files containing API keys
- Use strong passwords for user accounts
- Regularly backup your data using `genai-cli backup`
- Review audit logs periodically for suspicious activity
- Update sensitive PII policies in `config/policies.yaml`

---
**Version**: 1.0.0
**Last Updated**: December 2024
