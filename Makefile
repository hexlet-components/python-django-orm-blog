MANAGE := poetry run python manage.py

.PHONY: test
test:
	@poetry run pytest

.PHONY: setup
setup: db-clean install migrate

.PHONY: install
install:
	@poetry install

.PHONY: db-clean
db-clean:
	@rm db.sqlite3 || true

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus

.PHONY: lint
lint:
	@poetry run flake8 hexlet_django_orm_blog
