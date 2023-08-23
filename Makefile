
prod:
	$(make) -c ./master prod
	$(make) -c ./worker compact-prod
dev:
	$(make) -c ./master dev
	$(make) -c ./worker compact-dev
clean-dev:
	$(make) -c ./worker clean-compact-dev
	$(make) -c ./master clean-dev