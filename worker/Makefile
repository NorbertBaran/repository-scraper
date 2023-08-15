prod:
	docker compose -f docker-compose.yml --env-file env/prod.compose.env up -d --build
test:
	docker compose -f docker-compose.yml --env-file env/test.compose.env up -d --build
clean-test:
	docker compose -f docker-compose.yml --env-file env/test.compose.env down
	docker volume rm repository-scraping-worker-broker-volume