from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,
    set_refresh_cookies, unset_jwt_cookies
)
from .redis_client import get_redis

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
r = get_redis()

def user_key(username: str) -> str:
    return f"user:{username}"

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not password:
        return jsonify({"error": "username i password su obavezni"}), 400

    if r.exists(user_key(username)):
        return jsonify({"error": "Korisnik već postoji"}), 409

    # DEMO: password u redis (plain). Za produkciju: hash (bcrypt).
    r.hset(user_key(username), mapping={"username": username, "password": password})
    r.set(f"user:{username}:unread", 0)
    return jsonify({"message": "Registracija uspješna"}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    u = r.hgetall(user_key(username)) if username else {}
    if not u or u.get("password") != password:
        return jsonify({"error": "Pogrešan username ili password"}), 401

    access = create_access_token(identity=username)
    refresh = create_refresh_token(identity=username)

    resp = make_response(jsonify({"access_token": access}), 200)
    set_refresh_cookies(resp, refresh)  # HttpOnly cookie
    return resp

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user = get_jwt_identity()
    access = create_access_token(identity=user)
    return jsonify({"access_token": access}), 200

@auth_bp.post("/logout")
def logout():
    resp = make_response(jsonify({"message": "Logged out"}), 200)
    unset_jwt_cookies(resp)  # briše refresh cookie
    return resp