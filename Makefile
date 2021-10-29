black-check:
	black ./payu --check

black-format:
	black ./payu

mypy-check:
	mypy ./payu

flake-check:
	python3 -m flake8 ./payu

isort-check:
	isort -c

run-tests:
	python3 -m pytest ./payu

sort-imports:
	isort -y
	black ./payu

quality-check:
	@make -s black-check
	@make -s flake-check
	@make -s mypy-check
	@make -s run-tests

format-code:
	@make -s sort-imports
	@make -s run-tests

run-tox:
	@make -s quality-check
	tox