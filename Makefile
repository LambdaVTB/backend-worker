include .env
export

CODE = app

prepare:
	poetry install

shell:
	poetry shell

run-local-gatherer:
	poetry run python worker/news_gatherer/cron.py

run-local-parser:
	poetry run python worker/trends_parser/cron.py

run-local-generator:
	poetry run python worker/insight_generator/cron.py

format:
	isort ${CODE}
	black ${CODE}

lint:
	pylint ${CODE}


