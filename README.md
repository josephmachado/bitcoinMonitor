# Bitcoin Monitor

This is an ETL pipeline to pull bitcoin exchange data from [CoinCap API](https://docs.coincap.io/) and load it into our data warehouse. For more details check out the blog at https://startdataengineering.com/post/data-engineering-project-to-impress-hiring-managers/

## Architecture

![Arch](assets/images/bc_arch.png)

We use python to pull, transform and load data. Our warehouse is postgres. We also spin up a Metabase instance for our presentation layer.

All of the components are running as docker containers.
## Setup

### Pre-requisites

1. [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) v1.27.0 or later.
2. [AWS account](https://aws.amazon.com/).
3. [AWS CLI installed](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
4. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
### Local

We have a [`Makefile`](Makefile) with common commands. These are executed in the running container.

```bash
cd bitcoinmonitor
make up # starts all the containers
make ci # runs formatting, lint check, type check and python test
```

If the CI step passes you can go to http://localhost:3000 to checkout your Metabase instance.

You can connect to the warehouse with the following credentials

```bash
Host: warehouse
Database name: finance
```
The remaining configs are available in the [env](env) file.

Refer to [this doc](https://www.metabase.com/docs/latest/users-guide/07-dashboards.html) for creating a Metabase dashboard.

### Production

In production we will run the instances as containers. We have helper scripts in [deploy_helpers](deploy_helpers) for this.

You will need to have an `ubuntu x_86` EC2 instance with a custom TCP inbound rule with port `3000` open to the IP `0.0.0.0/0`. These can be set when you create an AWS EC2 instance in the `configure security group` section. A `t2.micro` (free-tier eligible) instance would be sufficient.

![Sec group](assets/images/bc_sec_gp.png)

You can setup a prod instance as shown below.

```bash
cd bitcoinmonitor

chmod 755 ./deploy_helpers/send_code_to_prod.sh

chmod 400 pem-full-file-location

./deploy_helpers/send_code_to_prod.sh pem-full-file-location EC2-Public-IPv4-DNS

# the above command will take you to your ubuntu instance.
# If you are having trouble connecting use method 2 from https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-fix-permission-denied-errors/

# install docker on your Ubuntu EC2 instance
chmod 755 install_docker.sh
./install_docker.sh
# verify that docker and docker compose installed
docker --version
docker-compose --version

# start the containers
unzip bitcoinmonitor.gzip && cd bitcoinmonitor/
docker-compose --env-file env up --build -d
```

## Tear down

You can spin down your local instance with.

```bash
make down
```

Do not forget to turn off your EC2 instance.