import os

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///election.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS / Security
    # Read CORS origins from env, support comma-separated lists and trim whitespace.
    _cors_raw = os.getenv("CORS_ORIGINS")
    if _cors_raw:
        CORS_ORIGINS = [o.strip() for o in _cors_raw.split(",") if o.strip()]
    else:
        # Default to common localhost dev origins (common dev ports)
        CORS_ORIGINS = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://[::1]:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
            "http://[::1]:3001",
        ]

    # Secret key for sessions/cookies (important if using credentials)
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
