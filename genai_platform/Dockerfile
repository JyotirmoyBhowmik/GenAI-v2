# GenAI Platform - Docker Deployment

FROM python:3.14-slim

LABEL maintainer="GenAI Platform Team"
LABEL description="Enterprise AI Orchestration Platform"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/chroma_db data/knowledge_graph data/mdm logs backups

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GENAI_PLATFORM_ENV=production

# Expose ports (if running API server)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from backend.config_manager import get_config; get_config()" || exit 1

# Initialize platform on startup
RUN python scripts/initialize.py || true

# Default command (can be overridden)
CMD ["python", "gui/main_window.py"]

# Alternative commands:
# CMD ["python", "-m", "uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["python", "-m", "backend.cli.main"]
