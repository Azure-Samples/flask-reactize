SHELL=/bin/bash

clean:
	@make clean --directory ../..

format:
	@isort .
	@black .

validate:
	@echo "Running 'isort'..."
	@isort --check ./src ./tests
	
	@echo "Running 'black'..."
	@black --check ./src ./tests
	
	@echo "Running 'flake8'..."
	@flake8 --statistics ./src ./tests
	
	@echo "All checks successfully passed!"

install-deps:
	pip install -r requirements.txt --quiet

unit-tests: install-deps
	@PYTHONPATH=./src python3 -m pytest ./tests --doctest-modules --cov=./src --junitxml=pytest-results.xml --cov-report term --cov-report=xml

dist: clean
	@PYTHONPATH=./src python3 setup.py sdist

pypi-upload:
	@python3 -m twine upload ./dist/*
