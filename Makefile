.PHONY: init lint test format precommit run

init:
	python3 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements-dev.txt && pre-commit install

lint:
	ruff check .

format:
	black . && isort . && ruff check --fix .

mypy:
	mypy .

test:
	pytest -q

run:
	python3 -m collabllm_sim.cli --help
