.PHONY: python-package help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([0-9a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

%:
    @:

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

docker-clean-unused: ## Remove unused Docker containers.
	docker system prune --all --force --volumes

docker-clean-all:  ## WATCH OUT! Remove *ALL* Docker containers, running or not.
	docker container stop $$(docker container ls --all --quiet) && docker system prune --all --force --volumes

build: ## Build the containers.
	docker-compose build

up: ## Start the services.
	docker-compose up

down:  ## Stop the services.
	docker-compose down --volumes

shell: ## Open up a shell in webserver.
	docker-compose run --publish 8080:8080 webserver /bin/sh

test:  ## Run tests.
	docker-compose run webserver pytest
