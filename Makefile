.PHONY: test lint run clean

test:
	pytest tests/ -v

lint:
	ruff check gravit_verifier/

run:
	uvicorn api.main:app --reload --port 8080

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

install:
	pip install -e .
