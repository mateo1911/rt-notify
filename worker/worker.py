import os
import json
import redis
from kafka import KafkaConsumer

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "notifications")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BOOTSTRAP],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="notif-consumers",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)

print("Worker started. Listening on topic:", TOPIC)

for msg in consumer:
    event = msg.value
    if event.get("type") == "NOTIFICATION_CREATED":
        to_user = event.get("to_user")
        if to_user:
            r.lpush(f"user:{to_user}:notifications", json.dumps(event))
            r.ltrim(f"user:{to_user}:notifications", 0, 49)
            r.incr(f"user:{to_user}:unread")
            print("Stored notification for:", to_user)