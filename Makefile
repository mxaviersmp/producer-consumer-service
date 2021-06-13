help:
	@echo "available commands"
	@echo " - venv              : creates the development environment"
	@echo " - clean             : clean temporary folders and files"
	@echo " - lint              : checks code style and type checks"
	@echo " - test              : runs all unit and integration tests"
	@echo " - coverage          : runs coverage report"
	@echo " - dev-producer      : starts producer api in development environment"
	@echo " - dev-consumer      : starts consumer in development environment"
	@echo " - build-containers  : pulls and builds docker containers for rabbitmq, producer and consumer"
	@echo " - start-containers  : starts docker containers for rabbitmq, producer and consumer"
	@echo " - stop-containers   : stop docker containers for rabbitmq, producer and consumer"
	@echo " - clean-all         : removes environment, volumes, containers and images"

venv:
	[ -d "./env" ] || ( \
		python -m venv env && \
		. env/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements-dev.txt && \
		pip install -e . && \
		pre-commit install && \
		((command -v gitmoji >/dev/null && gitmoji -i) || echo Please install gitmoji-cli) \
	)
	touch env/bin/activate

clean:
	rm -rf `find . -type d -name .pytest_cache`
	rm -rf `find . -type d -name .mypy_cache`
	rm -rf `find . -type d -name __pycache__`
	rm -rf `find . -type d -name .ipynb_checkpoints`
	rm -f .coverage

lint: venv clean
	. env/bin/activate; flake8; mypy

test: venv clean
	. env/bin/activate; pytest

coverage: venv clean
	. env/bin/activate; coverage run -m pytest; coverage report

dev-producer: venv
	. env/bin/activate; uvicorn app.producer.main:app --reload

dev-consumer: venv
	. env/bin/activate; python app/consumer/main.py

build-app:
	docker-compose pull
	docker-compose build

logs-app:
	docker-compose logs -f --tail 20

start-app: build-containers
	docker-compose up -d

stop-app:
	docker-compose stop

clean-all: clean
	rm -rf app.egg-info
	rm -rf db
	rm -rf env
	rm output.txt
	docker-compose down --rmi all
