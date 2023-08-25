up:
	docker compose up --build -d
down:
	docker compose down
rmi:
	docker compose down --rmi all
rmv:
	docker volume rm repository-scraping-postgres-volume repository-scraping-redis-volume
rma:
	make rmi rmv
up-client:
	docker compose -f docker-compose-client.yml up -d
down-client:
	docker compose -f docker-compose-client.yml down --rmi all