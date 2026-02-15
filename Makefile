.PHONY: test test-unit test-integration test-functional test-network env-up env-down

PYTHON := .venv/bin/python
PYTEST := $(PYTHON) -m pytest

# Default: unit + integration (offline)

test:
	$(PYTEST) -m "not functional"

test-unit:
	$(PYTEST) -m "unit"

test-integration:
	$(PYTEST) -m "integration"

test-functional:
	$(PYTEST) -m "functional"

test-network:
	$(PYTEST) -m "network"

env-up:
	./scripts/sync_env.sh up

env-down:
	./scripts/sync_env.sh down
