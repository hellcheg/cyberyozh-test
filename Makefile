run:
	docker compose up -d --build

integration-tests:
	docker compose --profile test run --build --rm tests coverage run manage.py test


unit-tests:
	pytest src/ -v --cov=.  --cov-report=term-missing