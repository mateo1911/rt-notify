import os
from flask import Flask, jsonify, render_template, redirect
from flask_jwt_extended import JWTManager
from .auth import auth_bp
from .notifications import notif_bp

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change_me")


    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_SECURE"] = False          
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False    
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev")
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notif_bp)
    @app.get("/")
    def home():
        return redirect("/login")

    @app.get("/register")
    def register_page():
        return render_template("register.html")

    @app.get("/login")
    def login_page():
        return render_template("login.html")

    @app.get("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app
    
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
    @app.get("/")
    def home():
        return redirect("/login")

    @app.get("/register")
    def register_page():
        return render_template("register.html")

    @app.get("/login")
    def login_page():
        return render_template("login.html")

    @app.get("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")