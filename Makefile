.PHONY: python-package help
.DEFAULT_GOAL := help


COMMAND = docker-compose -f docker-compose-LocalExecutor.yml run --volume $$(pwd)/requirements.txt:/requirements.txt --publish 8080:8080 -e S3_BUCKET=$(S3_BUCKET) -e NEWS_API_KEY=$(NEWS_API_KEY) -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) webserver
MODULE = src/dags

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

up: ## Start the services.
	docker-compose -f docker-compose-LocalExecutor.yml up --build

run: ## Run webserver.
	$(COMMAND)

shell: ## Open up a shell in webserver.
	docker-compose -f docker-compose-LocalExecutor.yml run --volume $$(pwd)/requirements.txt:/requirements.txt --publish 8080:8080 webserver /bin/sh

test:  ## Run tests.
	docker-compose -f docker-compose-LocalExecutor.yml run --volume $$(pwd)/requirements.txt:/requirements.txt webserver \
	/usr/local/airflow/.local/bin/pytest

clean:  ## Remove artifacts.
	find ${MODULE} | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	find src/tests | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	if [ -d ".pytest_cache" ]; then rm -r .pytest_cache; fi
	if [ -d ".coverage" ]; then rm  .coverage; fi
