# Bitcoin Monitor

This is an ETL pipeline with a dashboard as the presentation layer.

The exchange data is pulled every 5 min and loaded into our Postgres datawarehouse. The ETL script is [here](src/bitcoinmonitor/exchange_data_etl.py).

## Setup

1. Set up AWS Cli
2. Set up EC2

```bash
cd bitcoinmonitor
./deploy_helpers/send_code_to_prod.sh pem-file-full-location EC2-public-DNS
# you will be in the Ubuntu EC2 instance

# install docker on your Ubuntu EC2 instance
./deploy_helpers/install_docker.sh

# start the containers
docker-compose down
docker-compose up --build -d
```

## Create Dashboard

## Tear down