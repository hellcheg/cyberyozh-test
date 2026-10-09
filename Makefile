run:
	docker compose up -d

integration-test:
	docker compose run --rm web python manage.py test
