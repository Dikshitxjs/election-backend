from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize the database and create tables if they don't exist"""
    if not hasattr(app, "db_initialized"):
        db.init_app(app)
        app.db_initialized = True
        with app.app_context():
            try:
                db.create_all()  # creates tables if missing
                print("✅ Database initialized and tables ensured.")
            except Exception as e:
                print("❌ Error initializing database:", e)
