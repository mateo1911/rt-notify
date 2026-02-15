import os
import json
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

_producer = None

def _serializer(v):
    return json.dumps(v).encode("utf-8")

def get_topic():
    return os.getenv("KAFKA_TOPIC", "notifications")

def get_producer(retries: int = 30, delay: float = 2.0):
    global _producer
    if _producer is not None:
        return _producer

    bootstrap = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
    last_err = None

    for _ in range(retries):
        try:
            _producer = KafkaProducer(
                bootstrap_servers=[bootstrap],
                value_serializer=_serializer,
                request_timeout_ms=20000,
                api_version_auto_timeout_ms=20000,
                retries=5,
            )
            return _producer
        except NoBrokersAvailable as e:
            last_err = e
            time.sleep(delay)

    raise last_err or NoBrokersAvailable()