docker-spin-up:
	docker compose --env-file env up --build -d

sleeper:
	sleep 15

up: docker-spin-up sleeper warehouse-migration

down: 
	docker compose down

shell:
	docker exec -ti pipelinerunner bash

format:
	docker exec pipelinerunner python -m black -S --line-length 79 .

isort:
	docker exec pipelinerunner isort .

pytest:
	docker exec pipelinerunner pytest /code/test

type:
	docker exec pipelinerunner mypy --ignore-missing-imports /code

lint: 
	docker exec pipelinerunner flake8 /code 

ci: isort format type lint pytest

stop-etl: 
	docker exec pipelinerunner service cron stop

####################################################################################################################
# Set up cloud infrastructure

tf-init:
	terraform -chdir=./terraform init

infra-up:
	terraform -chdir=./terraform apply

infra-down:
	terraform -chdir=./terraform destroy

infra-config:
	terraform -chdir=./terraform output

####################################################################################################################
# Datawarehouse migration

db-migration:
	@read -p "Enter migration name:" migration_name; docker exec pipelinerunner yoyo new ./migrations -m "$$migration_name"

warehouse-migration:
	docker exec pipelinerunner yoyo develop --no-config-file --database postgres://sdeuser:sdepassword1234@warehouse:5432/finance ./migrations

warehouse-rollback:
	docker exec pipelinerunner yoyo rollback --no-config-file --database postgres://sdeuser:sdepassword1234@warehouse:5432/finance ./migrations

####################################################################################################################
# Port forwarding to local machine

cloud-metabase:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o "IdentitiesOnly yes" -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) -N -f -L 3001:$$(terraform -chdir=./terraform output -raw ec2_public_dns):3000 && open http://localhost:3001 && rm private_key.pem

####################################################################################################################
# Helpers

ssh-ec2:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) && rm private_key.pem