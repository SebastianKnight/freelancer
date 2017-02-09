include config/makefile

#============================
### START DEVELOPING ########
#============================

init: clean ## start virtual environment and install dev. requirements
	rm -fr $(VIRTUAL_ENV)
	virtualenv -p python3 $(VIRTUAL_ENV) --distribute
	$(MAKE) install

install: clean ## install development libs
	pip install -r requirements_dev.txt

run: ## run test manualy
	python kicad-diff ./test/resources/Netlist1.net ./test/resources/Netlist2.net

#============================
### TESTING #################
#============================

test: test-spec-coverage lint ## run test, lint

test-spec-coverage: ## run spec tests with coverage
	coverage run --source ./$(PACKAGE) -m py.test test/spec
	coverage report -m
	coverage html

test-spec: ## run spec tests
	pytest test/spec

test-e2e: ## run e2e tests
	py.test test/e2e

lint: ## check style with pylint
	pylint --reports=n --output-format=colorized ./$(PACKAGE) ./tests

dep: ## test dependencies
	pip list --outdated --format=columns
	@if [ -z "$$(pip list --outdated --format=columns)" ]; then exit 0; else exit 1; fi

#============================
### CLEANING ################
#============================

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr deb_dist/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.tar.gz' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage coverage.xml
	rm -fr htmlcov/
