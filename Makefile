black-check:
	black ./payu --check

mypy-check:
	mypy ./payu

flake-check:
	python3 -m flake8 ./payu

run-tests:
	python3 -m pytest ./payu

quality-check:
	@make -s black-check
	@make -s flake-check
	@make -s mypy-check
	@make -s run-tests

run-tox:
	@make -s quality-check
	tox