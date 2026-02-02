import os
import re

class Config:
    # -----------------------
    # Database
    # -----------------------
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///election.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------
    # CORS / Security
    # -----------------------
    # Read CORS origins from environment variable 
    _cors_raw = os.getenv("CORS_ORIGINS")

    if _cors_raw:
        CORS_ORIGINS = [o.strip() for o in _cors_raw.split(",") if o.strip()]
    else:
       
        CORS_ORIGINS = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://[::1]:3000",
            "https://nepalelection.vercel.app",  
        ]

    # Optional: Regex to allow any LAN dev IP on port 3000
    CORS_ORIGIN_REGEX = re.compile(
        r"^http://(localhost|127\.0\.0\.1|\[::1\]|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}):3000$"
    )

    # -----------------------
    # Secret key
    # -----------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
