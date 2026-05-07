````markdown
# 🧪 OSINT CrewAI - Testing Guide

Comprehensive testing guide for OSINT CrewAI project.

## Table of Contents

1. [Unit Testing](#unit-testing)
2. [Integration Testing](#integration-testing)
3. [End-to-End Testing](#end-to-end-testing)
4. [CI/CD Integration](#cicd-integration)
5. [Performance Testing](#performance-testing)

---

## Unit Testing

### Setup

```bash
pip install pytest pytest-cov pytest-asyncio
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tools.py -v
```

### Test Structure

```
tests/
├── __init__.py
├── test_config.py
├── test_tools.py
├── test_agents.py
├── test_tasks.py
└── test_crew.py
```

### Example Tests

```python
# tests/test_tools.py
import pytest
from src.tools import EmailTools, IPTools, DomainTools

class TestEmailTools:
    def test_valid_email(self):
        assert EmailTools.is_valid_email("user@example.com") == True
        assert EmailTools.is_valid_email("invalid.email") == False
    
    def test_extract_domain(self):
        domain = EmailTools.extract_domain("user@example.com")
        assert domain == "example.com"

class TestIPTools:
    def test_valid_ip(self):
        assert IPTools.is_valid_ip("8.8.8.8") == True
        assert IPTools.is_valid_ip("invalid.ip") == False

class TestDomainTools:
    def test_valid_domain(self):
        assert DomainTools.is_valid_domain("example.com") == True
        assert DomainTools.is_valid_domain("invalid") == False
```

---

## Integration Testing

### Test Full Workflow

```bash
# Test email investigation
python osint-crewai/main.py --target "test@example.com" --output json

# Test IP investigation
python osint-crewai/main.py --target "8.8.8.8" --output markdown

# Test domain investigation
python osint-crewai/main.py --target "example.com" --verbose
```

### Validate Output

```bash
# Check generated files
ls -la outputs/

# Verify JSON format
python -m json.tool outputs/osint_*.json

# Check markdown syntax
cat outputs/osint_*.md | head -20
```

---

## End-to-End Testing

### Docker Testing

```bash
# Build test image
docker build -t osint-crewai:test .

# Run test
docker run --env-file .env osint-crewai:test \
    --target "example@email.com" \
    --output json

# Verify outputs
docker run --env-file .env -v $(pwd)/outputs:/app/outputs \
    osint-crewai:test ls -la /app/outputs/
```

### Docker Compose Testing

```bash
# Run investigation
docker-compose run --rm osint-crewai \
    --target "example@email.com" \
    --verbose

# Verify output
docker-compose exec osint-crewai ls -la /app/outputs/
```

---

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest tests/ -v --cov=src
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

### Docker Build Test

Create `.github/workflows/docker.yml`:

```yaml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t osint-crewai:latest .
    
    - name: Test image
      run: |
        docker run osint-crewai:latest --help
```

---

## Performance Testing

### Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py
from locust import HttpUser, task

class OSINTUser(HttpUser):
    @task
    def investigate(self):
        self.client.post("/osint", json={"target": "example@email.com"})

# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

### Response Time Testing

```python
import time
from src.crew import OsintCrew

start = time.time()
crew = OsintCrew("user@example.com")
result = crew.run()
end = time.time()

print(f"Execution time: {end - start:.2f}s")
```

---

## Continuous Monitoring

### Health Checks

```bash
# Check service status
curl http://localhost:8000/health

# Monitor logs
docker-compose logs -f osint-crewai

# Track performance
watch -n 5 'docker stats osint-crewai'
```

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-07
````