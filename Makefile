run:
	docker compose up -d --build

integration-test:
	docker compose run --rm web python manage.py test
