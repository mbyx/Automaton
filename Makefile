default:
	$(MAKE) fmt
	{ $(MAKE) check & $(MAKE) test; }

# Formats the project using black and sorts imports using isort.
fmt:
	poetry run black .
	poetry run isort .

# Checks the code for type errors and bad practices using mypy and flake8.
check:
	{ poetry run flake8 . & poetry run mypy automaton; }

# Runs the test suite in tests/ via pytest.
test:
	poetry run pytest automaton
