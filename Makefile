.PHONY: clean install versions lint test cov format

default: clean install

clean:
	find . -name '__pycache__' -exec rm -rf {} +
	rm -Rf build/

versions:
	pip-compile --extra dev --no-emit-index-url --upgrade -o requirements-dev.txt pyproject.toml

install:
	pip install -r requirements-dev.txt -e .

lint:
	black --check src tests
	ruff check src tests --preview
	mypy .

test:
	pytest

cov:
	pytest --cov=update_netrc --cov-report=html --cov-report=term

format:
	black --preview src tests
	ruff check src tests --preview --fix

wheel:
	pip wheel . -w dist

publish-release-testpypi: wheel
	twine upload --repository testpypi dist/*

publish_release: build_release
	twine upload dist/*
