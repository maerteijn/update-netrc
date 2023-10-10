.PHONY: clean install versions lint test cov format dist publish-release-pypi-test publish_release-pypi

default: clean install

clean:
	find . -name '__pycache__' -exec rm -rf {} +
	rm -Rf build/

versions:
	pip-compile --extra dev --no-emit-index-url --upgrade -o requirements-dev.txt pyproject.toml

install:
	pip install -r requirements-dev.txt -e .[dist]

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

dist:
	pyproject-build .

publish-release-pypi-test: dist
	twine upload --repository testpypi dist/*

publish_release-pypi: build_release
	twine upload dist/*

