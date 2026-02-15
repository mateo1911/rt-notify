import time
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .redis_client import get_redis
from .kafka_client import get_producer, get_topic
import json

notif_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

r = get_redis()
producer = get_producer()
TOPIC = get_topic()

@notif_bp.post("")
@jwt_required()
def create_notification():
    sender = get_jwt_identity()
    data = request.get_json() or {}

    to_user = (data.get("to_user") or "").strip()
    message = (data.get("message") or "").strip()

    if not to_user or not message:
        return jsonify({"error": "to_user i message su obavezni"}), 400

    event = {
        "type": "NOTIFICATION_CREATED",
        "to_user": to_user,
        "from_user": sender,
        "message": message,
        "ts": int(time.time()),
    }

    producer.send(TOPIC, event)
    producer.flush()
    return jsonify({"message": "Notifikacija poslana (Kafka)", "event": event}), 201

@notif_bp.get("")
@jwt_required()
def list_notifications():
    user = get_jwt_identity()
    raw = r.lrange(f"user:{user}:notifications", 0, 19)
    items = [json.loads(x) for x in raw]
    return jsonify(items)

@notif_bp.get("/unread-count")
@jwt_required()
def unread_count():
    user = get_jwt_identity()
    cnt = int(r.get(f"user:{user}:unread") or 0)
    return jsonify({"user": user, "unread": cnt})

@notif_bp.post("/mark-read")
@jwt_required()
def mark_read():
    user = get_jwt_identity()
    r.set(f"user:{user}:unread", 0)
    return jsonify({"message": "Označeno kao pročitano"})