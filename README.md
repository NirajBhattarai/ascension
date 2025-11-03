## Ascension Backend

Minimal Starlette server with a single health endpoint.

### A2A-style layout (no implementation)

```
backend/
  agents/
  app/
    cmd/
  client/
  models/
  server/
  tests/
```

Use `tests/` for TDD; keep code minimal until tests drive implementation.

### Setup (virtual environment)

macOS/Linux (zsh/bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
# Install project dependencies defined in pyproject.toml
pip install .
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .
```

### Run

```bash
python backend/server.py
```

### Endpoint

- GET `/health` → `{ "status": "ok" }`

### Test-Driven Development (TDD)

1) Install test tools in your venv:

```bash
pip install pytest
```

2) Create `tests/test_health.py` with a minimal test:

```python
from starlette.testclient import TestClient
from backend.server import app


def test_health_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

3) Run tests:

```bash
pytest -q
```

Workflow: write a failing test, implement the minimal change in `backend/server.py`, run tests, and refactor as needed.



# ascension
adk run seq_adk_agent