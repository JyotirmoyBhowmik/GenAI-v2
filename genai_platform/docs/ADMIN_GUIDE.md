# GenAI Platform — Administrator Guide

## Overview

This guide covers administrative tasks, configuration, deployment, and operational procedures for managing the GenAI Platform.

## Installation & Deployment

### Docker Deployment (Recommended)

```bash
docker-compose up -d
```

This starts:
- Main application
- ChromaDB (vector database)
- Neo4j (optional knowledge graph)

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize
python scripts/initialize.py

# Start application
python gui/main_window.py
```

### Server Deployment

```bash
genai-cli server --host 0.0.0.0 --port 8000
```

Accessible at: `http://<server-ip>:8000/api/docs`

## User Management

### Creating Users
```bash
genai-cli init  # Creates default admin user
```

To create additional users via code:
```python
from backend.mdm.user_manager import UserManager

um = UserManager()
user = um.create_user(
    username='analyst1',
    email='analyst@company.com',
    division_id='fmcg',
    department_id='fmcg_finance',
    role_id='analyst',
    full_name='Finance Analyst'
)
um.set_password('analyst1', 'SecurePassword@123')
```

### Managing Roles
- Edit `config/policies.yaml`
- Roles: super_admin, division_admin, department_admin, analyst, viewer
- Define permissions for each role

### User Permissions
Assign permissions in `config/policies.yaml`:
```yaml
roles:
  - id: analyst
    permissions:
      - ingest_files
      - query
      - view_audit_logs
      - access_connectors
```

## Configuration Management

### Divisions & Departments
Edit `config/divisions.yaml`:
```yaml
divisions:
  - id: fmcg
    name: FMCG Division
    departments:
      - id: sales
        name: Sales Department
```

### Models Configuration
Edit `config/models.yaml` to:
- Add new AI models
- Configure pricing
- Set default models per persona
- Enable/disable models

### Personas
Edit `config/personas.yaml` to create custom personas:
```yaml
personas:
  - id: custom_analyst
    name: Custom Analyst
    system_prompt: "You are a custom business analyst..."
    allowed_models: [gpt-4, claude-3-sonnet]
    capabilities: [query, analysis, reporting]
```

### Policies & Compliance
Edit `config/policies.yaml` for:
- PII detection patterns
- Data retention policies
- Audit requirements
- Compliance rules

## Data Management

### Backup & Recovery

**Create Backup:**
```bash
genai-cli backup
# Or via BackupManager in code
```

**List Backups:**
```bash
python scripts/restore.py --list
```

**Restore Backup:**
```bash
python scripts/restore.py --backup-id <backup-id>
```

### Data Ingestion

```bash
genai-cli generate --division fmcg --count 1000
```

Generate sample data for testing and development.

### Database Maintenance

```bash
# Check database status
genai-cli health

# Run cleanup scripts (if any)
python scripts/maintenance.py
```

## Monitoring & Auditing

### System Health
```bash
genai-cli health
```

Checks:
- Configuration loading
- User management system
- Model availability
- Database connectivity

### Audit Logs

Access audit logs via API:
```bash
curl http://localhost:8000/api/audit/logs?user_id=admin
```

Or programmatically:
```python
from backend.governance.audit_trail import AuditTrailSystem

audit = AuditTrailSystem()
logs = audit.query_logs(division_id='fmcg', limit=100)
```

### Cost Tracking

View costs by division:
```python
from backend.billing.billing_engine import BillingEngine, CostTracker

tracker = CostTracker()
costs = tracker.get_costs(division_id='fmcg')
total = tracker.get_total_cost(division_id='fmcg')
```

## Security & Compliance

### PII Protection

Configure PII detection in `config/policies.yaml`:
```yaml
pii_policies:
  pii_types:
    - name: email
      pattern: '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
      sensitivity: high
```

### Encryption

Configure in `.env`:
```env
ENCRYPTION_KEY=your-base64-encoded-key
ENCRYPTION_AT_REST=True
```

### Access Control

Set role-based access:
```python
from backend.security.rbac import RBACManager

rbac = RBACManager()
can_access = rbac.can_access_division(
    role_id='analyst',
    division_id='fmcg',
    user_division='fmcg'
)
```

## Troubleshooting

### High Memory Usage
- Reduce vector database size
- Archive old data
- Restart services regularly

### Slow Queries
- Index knowledge graph entities
- Enable query caching
- Use appropriate embedding models

### Model Failures
- Check API keys in `.env`
- Verify internet connectivity
- Test with: `genai-cli health`
- Switch to local models (Ollama) for offline

### Backup Issues
- Ensure sufficient disk space
- Check backup directory permissions
- Verify database connectivity

## Disaster Recovery

### Quick Recovery Procedure
1. Stop the application
2. Restore from backup: `python scripts/restore.py --backup-id <id>`
3. Verify data: `genai-cli health`
4. Restart application

### Partial Recovery
Restore individual components:
```python
from backend.backup.backup_manager import BackupManager

manager = BackupManager()
manager.restore_vector_db(backup_path)
manager.restore_knowledge_graph(backup_path)
manager.restore_warehouse(backup_path)
```

## Scaling & Performance

### Horizontal Scaling
- Deploy multiple API servers behind a load balancer
- Use shared vector database (Pinecone, Weaviate)
- Use shared knowledge graph (Neo4j)
- Use shared SQL warehouse (PostgreSQL, MySQL)

### Performance Tuning
1. Enable query caching
2. Use batch ingestion
3. Archive old data
4. Optimize embedding models
5. Use connection pooling for databases

## Updates & Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Version Management
Check current version:
```bash
genai-cli version
```

### Zero-Downtime Deployment
1. Update code on secondary server
2. Run tests
3. Switch load balancer to new server
4. Update primary server

---
**Version**: 1.0.0
**Last Updated**: December 2024
