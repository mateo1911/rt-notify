import os
import json
from kafka import KafkaProducer

def _serializer(v):
    return json.dumps(v).encode("utf-8")

def get_producer():
    return KafkaProducer(
        bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")],
        value_serializer=_serializer,
    )

def get_topic():
    return os.getenv("KAFKA_TOPIC", "notifications")