up:
	docker compose up --build -d
down:
	docker compose down
rmi:
	docker compose down --rmi all
rmv:
	docker volume rm repository-scraping-redis-volume repository-scraping-worker-logs-volume
rma:
	make rmi rmv