import os
import re

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Ensure instance folder exists
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(INSTANCE_DIR, 'election.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS configuration
    _cors_raw = os.getenv("CORS_ORIGINS")
    CORS_ORIGINS = (
        [o.strip() for o in _cors_raw.split(",") if o.strip()]
        if _cors_raw
        else [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://[::1]:3000",
            "https://nepalelection.vercel.app",
        ]
    )

    CORS_ORIGIN_REGEX = re.compile(
        r"^http://(localhost|127\.0\.0\.1|\[::1\]|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}):3000$"
    )

    # Application secret key
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
