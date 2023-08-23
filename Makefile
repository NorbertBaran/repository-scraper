up:
	docker compose up --build -d
down:
	docker compose down --rmi
clean:
	docker volume rm repository-scraping-redis-volume repository-scraping-postgres-volume