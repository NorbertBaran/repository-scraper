prod:
	docker compose up --build -d
dev:
	docker compose up -f docker-compose.yml -f docker-compose.client.yml --build -d
clean-dev:
	docker compose -f docker-compose.yml -f docker-compose.client.yml down --rmi
	docker volume rm repository-scraping-postgres-volume repository-scraping-redis-volume