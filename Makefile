api-dev:
	cd src; python -m univer_api

api:
	docker compose --env-file .env -f devops/docker-compose.yaml -p univer up --build --detach api

admin-dev:
	cd src; python -m admin.main

admin:
	docker compose --env-file .env -f devops/docker-compose.yaml -p univer up --build --detach admin

db:
	docker compose --env-file .env -f devops/docker-compose.yaml -p univer up --build --detach db

up:
	docker compose --env-file .env -f devops/docker-compose.yaml -p univer up --build

down:
	docker compose --env-file .env -f devops/docker-compose.yaml -p univer down

install:
	pip install --upgrade pip
	pip install -r requirements.txt

create-db:
	cd src; python -m scripts.create_db

add-table:
	cd src; python -m scripts.add_table $(t) ../$(f)

drop-db:
	cd src; python -m scripts.drop_db

create-example: create-db
	cd src; python -m scripts.create_example

add-all-data:
	make add-table t=teachers f=data/csv_data/teachers.csv
	make add-table t=classrooms f=data/csv_data/lessons.csv
	make add-table t=subjects f=data/csv_data/lessons.csv
	make add-table t=groups f=data/csv_data/groups.csv
	make add-table t=lessons f=data/csv_data/lessons.csv

parse-schedule:
	cd src; python -m scripts.parse_schedule --html=../$(html) --group=$(group) --subgroup=$(subgroup)

generate-secret:
	cd src; python -m scripts.generate_secret

revision:
	cd src; alembic revision --autogenerate

migrate:
	cd src; alembic upgrade head
