from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.database.db import db, init_db
from app.routes import register_routes
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Initialize DB
    init_db(app)

    # Migrations
    Migrate(app, db)

    # --- CORS ---
    cors_origins = getattr(app.config, "CORS_ORIGINS", ["http://localhost:3000"])
    CORS(
        app,
        resources={r"/api/*": {"origins": cors_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # --- Health / Root routes ---
    @app.route("/")
    def root():
        return {"service": "Election 2082 API", "status": "running"}, 200

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    # --- Register all blueprints ---
    register_routes(app)

    return app
