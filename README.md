# Bitcoin Monitor

This is an ETL pipeline with a dashboard as the presentation layer.

The exchange data is pulled every 5 min and loaded into our Postgres datawarehouse. The ETL script is [here](src/bitcoinmonitor/exchange_data_etl.py).

## Setup

1. Set up AWS Cli
2. Set up EC2

```bash
cd bitcoinmonitor
chmod 755 ./deploy_helpers/send_code_to_prod.sh

# send the code to your EC2
# if you get "Permission denied (publickey)", use method 2 from https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-fix-permission-denied-errors/
./deploy_helpers/send_code_to_prod.sh pem-file-full-location EC2-Public-IPv4-DNS
# you will be in your Ubuntu EC2 instance

# install docker on your Ubuntu EC2 instance
chmod 755 install_docker.sh
./install_docker.sh

# start the containers
cd bitcoinmonitor
docker-compose down
docker-compose up --build -d
```

## Create Dashboard

## Tear down