"""Run Alembic migrations programmatically.

This script initializes the migrations folder (if missing), autogenerates a migration,
and applies it (upgrade) against whichever `DATABASE_URL` is configured in env.

USAGE: set `DATABASE_URL` in your environment to the Supabase/Postgres URL, then run:
    python run_migrations.py

Note: You must install `Flask-Migrate` (added to `requirements.txt`).
"""
import os
from app import create_app
from app.database.db import db
from flask_migrate import Migrate, init as m_init, migrate as m_migrate, upgrade as m_upgrade


def main():
    app = create_app()
    migrate = Migrate(app, db)

    with app.app_context():
        migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
        # Initialize migrations directory if missing
        if not os.path.exists(migrations_dir):
            print("Initializing migrations folder...")
            m_init()

        print("Autogenerating migration...")
        m_migrate(message="autogenerate")

        print("Applying migrations (upgrade)...")
        m_upgrade()

        print("Migrations complete.")


if __name__ == "__main__":
    main()
