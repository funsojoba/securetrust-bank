build:
	docker compose up --build -d --remove-orphans

up:
	docker-compose up -d

down:
	docker-compose down

show-logs-api_gateway:
	docker compose logs api-gateway

show-logs-user_account:
	docker compose logs user-account-service

show-logs-user_account_db:
	docker compose logs user-account-db

show-logs-redis:
	docker compose logs redis

show-logs-rabbitmq:
	docker compose logs rabbitmq

redis-cli:
	docker-compose exec redis redis-cli

superuser:
	docker compose exec -it user-account-service python manage.py createsuperuser
