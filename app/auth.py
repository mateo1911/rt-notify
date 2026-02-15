from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .redis_client import get_redis

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
r = get_redis()

def user_key(username: str) -> str:
    return f"user:{username}"

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not password:
        return jsonify({"error": "username i password su obavezni"}), 400

    if r.exists(user_key(username)):
        return jsonify({"error": "Korisnik već postoji"}), 409

    
    r.hset(user_key(username), mapping={"username": username, "password": password})
    r.set(f"user:{username}:unread", 0)
    return jsonify({"message": "Registracija uspješna"}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    u = r.hgetall(user_key(username)) if username else {}
    if not u or u.get("password") != password:
        return jsonify({"error": "Pogrešan username ili password"}), 401

    token = create_access_token(identity=username)
    return jsonify({"access_token": token})