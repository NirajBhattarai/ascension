UV=uv

.PHONY: uv-venv uv-sync install run run-agent test clean format

uv-venv:
	$(UV) venv --python 3.11 || true

uv-sync: uv-venv
	$(UV) sync --all-extras --dev

install: uv-sync

run: uv-sync
	$(UV) run python backend/server/server.py

run-agent: uv-sync
	$(UV) run python backend/agent.py

test: uv-sync
	$(UV) run pytest -q

format: uv-sync
	$(UV) run isort backend
	$(UV) run black backend

clean:
	rm -rf .venv
	find . -name "__pycache__" -type d -exec rm -rf {} +


