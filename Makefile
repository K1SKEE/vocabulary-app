init: down docker-pull docker-build up
up: docker-up
down: docker-down
restart: down up

docker-up:
	docker-compose up -d
docker-down:
	docker-compose down --remove-orphans
docker-pull:
	docker-compose pull
docker-build:
	docker-compose build