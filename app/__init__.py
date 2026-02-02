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

# --------------------------
# CORS Configuration
# --------------------------
# Use environment variable CORS_ORIGINS if set, else allow localhost
cors_origins = os.environ.get("CORS_ORIGINS")
if cors_origins:
    # support multiple origins comma-separated
    cors_origins = [origin.strip() for origin in cors_origins.split(",")]
else:
    cors_origins = ["http://localhost:3000"]

# Apply CORS safely
CORS(
    app,
    resources={r"/*": {"origins": cors_origins}},
    supports_credentials=True,  # allow cookies/auth headers
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=86400
)

# --------------------------
# Root / Health routes
# --------------------------
@app.route("/")
def root():
    return {"service": "Election 2082 API", "status": "running"}, 200

@app.route("/health")
def health():
    return {"status": "ok"}, 200

# --------------------------
# Register Blueprints
# --------------------------
register_routes(app)

# --------------------------
# Run app locally
# --------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
