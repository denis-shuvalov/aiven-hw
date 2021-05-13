The application is a web service with WEB API 
for access to Kafka and PostgresSQL in the cloud platform of Aiven.

The service based on AIOHTTP Python framework.

- Producer is made as an API view and model and allows to send messages 
to Kafka via GET request.
- Consumer is managed by 2 API handlers - start and stop.
The consumer works as an Asyncio Task.
- Also there is API for Postgres view. 

## Preparation

- Clone the GIT repo.
- Create a directory named 'cert' in the root of project and put following files there:
ca.pem, service.cert and service.key (files from Aiven).
Names of the files should be the same. (This can be changed in the file 'settings.py').
- Create '.env' file and put following variables with corresponding values there:
`ENVIRONMENT=aiven`\
`KAFKA_BOOTSTRAP_SERVER=your_aiven_kafka_host:port`\
`POSTGRES_URL=postgres://user:pass@aiven-host:port/db...`
- Create virtualenv and install requirements (it is necessary for migrations):
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
- Create topic 'home-work' in your Aiven Kafka.
- Create database 'event_storage' in your Aiven Postgres.

## Local test and start

- Local services start (Kafka and Postgres). Use 'sudo' if it's necessary.
```
docker-compose -f db.docker-compose.yml up
```
- Make migrations:
```
yoyo apply
```
- Build test container:
```
docker build -f test.Dockerfile -t hw_test .
```
- Run test container:
```
docker run --rm --network=rmoff_kafka --name hwt hw_test
```
- Build and run main container:
```
docker build -f Dockerfile -t hw_app .
docker run --rm --network=rmoff_kafka -p 8080:8080 --name hw hw_app
```

## Run with Aiven services

- Test
```
docker build -f test.Dockerfile -t hw_test .
docker run --env-file .env --rm --name hwt hw_test
```
- Run
```
docker build -f Dockerfile -t hw_app .
docker run --rm --env-file .env -p 8080:8080 --name hw hw_app
```

## Usage

Go to web browser (Chromium/Chrome preferable).

- Start consumer: \
http://0.0.0.0:8080/api/v1/consumer/start

- Write message to producer: \
http://0.0.0.0:8080/api/v1/producer/send?message=test_message

Message is a parameter of GET request 'message'.

- Inspect Postgres: \
http://0.0.0.0:8080/api/v1/postgres/events?num_events=10

'num_events' - GET parameter which shows how much events should be shown.
The first message in the list - the last message.

## Used resources 

- Confluent \
https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/

- Aiokafka docs \
https://aiokafka.readthedocs.io/en/stable/
- Asyncpg docs \
https://magicstack.github.io/asyncpg/current/
- Aiohttp docs \
https://docs.aiohttp.org/en/stable/
- Aiven articles. 
