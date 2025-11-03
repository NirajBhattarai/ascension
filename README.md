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

### Setup

macOS/Linux (zsh/bash):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.11
uv sync --all-extras --dev
```

Windows (PowerShell):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
uv venv --python 3.11
uv sync --all-extras --dev
```

### Run server

```bash
# With uv
make run

# Direct (without Makefile)
uv run python backend/server/server.py
```

### Run agent (simulate pipeline)

```bash
# With uv
make run-agent

# Direct (without Makefile)
uv run python backend/agent.py
```

### Endpoint

- GET `/health` → `{ "status": "ok" }`

### Test-Driven Development (TDD)

1) Create `tests/test_health.py` with a minimal test:

```python
from starlette.testclient import TestClient
from backend.server import app


def test_health_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

2) Run tests:

```bash
make test
# or
uv run pytest -q
```

Workflow: write a failing test, implement the minimal change in `backend/server.py`, run tests, and refactor as needed.



# ascension
adk run seq_adk_agent