format:
	python -m black .
	python -m isort .

lint:
	python -m black --check --diff .
	python -m isort --check --diff .
	pylint

test:
	pytest

.PHONY: lint format test
