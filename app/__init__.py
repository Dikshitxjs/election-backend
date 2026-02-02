from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.database.db import db, init_db
from app.routes import register_routes
import os

app = Flask(__name__)
app.config.from_object("app.config.Config")

# Initialize DB
init_db(app)
Migrate(app, db)

# CORS
CORS(app, resources={r"/*": {"origins": getattr(app.config, 'CORS_ORIGINS', ['http://localhost:3000'])}})

# Root / Health
@app.route("/")
def root():
    return {"service": "Election 2082 API", "status": "running"}, 200

@app.route("/health")
def health():
    return {"status": "ok"}, 200

# Blueprints
register_routes(app)

# Only run when testing locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
