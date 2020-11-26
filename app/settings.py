import os

ENVIRONMENT = os.getenv("ENVIRONMENT", default="local")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", default="broker:9092")
KAFKA_TOPIC = "home-work"
POSTGRES_URL = os.getenv("POSTGRES_URL", default="postgresql://postgres:qwerty@postgres:5432/event_storage")

POSTGRES_TABLE = "kafka_events"
SSL_CAFILE_KAFKA = "cert/ca.pem"
SSL_CERTFILE_KAFKA = "cert/service.cert"
SSL_KEYFILE = "cert/service.key"
