import os


KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", default="broker:9092")
KAFKA_TOPIC = "home-work"
POSTGRES_URL = os.getenv("POSTGRES_URL", default="postgresql://postgres:qwerty@0.0.0.0:5432/event_storage")


