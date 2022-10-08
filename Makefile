include .env
export

CODE = app

prepare:
	poetry install

shell:
	poetry shell

run-local:
	poetry run python worker/news_gatherer/cron.py

format:
	isort ${CODE}
	black ${CODE}

lint:
	pylint ${CODE}


