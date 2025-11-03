PYTHON=python3
VENV=.venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python
PYTEST=$(VENV)/bin/pytest

.PHONY: venv install run test clean

venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install .
	$(PIP) install pytest

run: install
	$(PY) backend/server/server.py

test: install
	$(PYTEST) -q

clean:
	rm -rf $(VENV)
	find . -name "__pycache__" -type d -exec rm -rf {} +


