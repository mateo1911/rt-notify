import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from .auth import auth_bp
from .notifications import notif_bp

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev")
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notif_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)