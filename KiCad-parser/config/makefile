VIRTUAL_ENV = virtualenv
PATH := $(VIRTUAL_ENV)/bin:$(PATH)

.PHONY: clean clean-test clean-pyc clean-build docs help test
.DEFAULT_GOAL := help

PACKAGE = kicad-diff
NOW_DATE=`date +%Y-%m-%d %H:%M:%S`

define PRINT_HELP_PYSCRIPT
import re, sys
for line in sys.stdin:
	match = re.match(r'^### (.*) #', line)
	if match:
		target = match.groups()[0]
		print("\n%s" % (target))
	match = re.match(r'^([a-zA-Z0-9_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("  %-15s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
