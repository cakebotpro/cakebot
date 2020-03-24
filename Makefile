start:
	python3 main.py
.PHONY: start

devshell:
	python3 main.py shell
.PHONY: devshell

format:
	python3 -m black --line-length 78 main.py
	python3 -m black --line-length 78 club/cakebot/*.py
.PHONY: format

test:
	python3 tests.py
.PHONY: test

test-and-report:
	python3 -m xmlrunner tests
.PHONY: test-and-report

lint:
	python3 -m mypy -m main
	python3 -m flake8 *.py
	python3 -m flake8 club/cakebot/*.py
.PHONY: lint

deps:
	python3 -m pip install --upgrade -r requirements.txt
.PHONY: deps
