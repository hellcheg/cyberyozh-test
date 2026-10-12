run:
	docker compose up -d --build

integration-tests:
	docker compose --profile test run --build --rm tests coverage run manage.py test --verbosity=2


unit-tests:
	docker compose --profile test run --build --rm tests pytest . -v --cov=.  --cov-report=term-missing