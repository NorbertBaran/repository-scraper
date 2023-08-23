compact-prod:
	docker compose --profile compact up --build -d
compact-dev:
	docker compose --profile compact up --build -d
clean-compact-dev:
	docker compose --profile compact down --rmi

masterless-prod:
	docker compose --profile masterless up --build -d
masterless-dev:
	docker compose --profile masterless up --build -d
clean-masterless-dev:
	docker compose --profile masterless down --rmi
	docker volume rm repository-scraping-redis-volume