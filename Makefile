start-dev:
	python3 -m uvicorn app.main:app --reload

start:
	python3 -m uvicorn app.main:app

# Initialize your local database
psql-up:
	sudo systemctl stop postgresql
	docker compose -f .docker/docker-compose.yml up -d --build --force-recreate --remove-orphans db
	python3 app/create_data.py

# Remove your local database
psql-down:
	sudo docker compose -f .docker/docker-compose.yml down -v --remove-orphans

psql-restart:
	sudo docker compose -f .docker/docker-compose.yml down -v --remove-orphans
	docker compose -f .docker/docker-compose.yml up -d --build --force-recreate --remove-orphans db