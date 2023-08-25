up:
	docker compose up --build -d
down:
	docker compose down
rmi:
	docker compose down --rmi all
rmv:
	docker volume rm repository-scraping-redis-volume repository-scraping-postgres-volume
rma:
	make rmi rmv
up-client:
	docker compose -f master/docker-compose-client.yml up -d
down-client:
	docker compose -f master/docker-compose-client.yml down --rmi all