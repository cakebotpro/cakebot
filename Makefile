test:
	python3 tests.py
.PHONY: test

test-and-report:
	python3 -m xmlrunner tests
.PHONY: test-and-report

format:
	python3 -m isort -rc .
	python3 -m black --line-length 78 main.py
	python3 -m black --line-length 78 tests.py
	python3 -m black --line-length 78 cakebot/*.py
.PHONY: format

lint:
	python3 -m mypy -m main
	python3 -m mypy -m tests
	python3 -m flake8 *.py
	python3 -m flake8 cakebot/*.py
.PHONY: lint

deps:
	python3 -m pip install --upgrade -r requirements.txt
.PHONY: deps

clean:
	rm -rf .mypy_cache __pycache__ cakebot/__pycache__
.PHONY: clean
