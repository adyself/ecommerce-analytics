.PHONY: up down logs etl gen

up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

etl:
	docker-compose run --rm etl python src/etl/run.py --stage all

gen:
	python data/synthetic/generate_data.py
