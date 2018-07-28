env:
	virtualenv env

.PHONY:
lint: env
	./env/bin/python -m flake8 talons/ test/

.PHONY:
test: env lint
	./env/bin/python -m pytest
