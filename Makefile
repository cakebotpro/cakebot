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
