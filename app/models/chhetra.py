from app.database.db import db

class Chhetra(db.Model):
    __tablename__ = "chhetras"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    region = db.Column(db.String(120), nullable=True)

    # Relationship (optional but useful)
    candidates = db.relationship(
        "Candidate",
        backref="chhetra",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "region": self.region,
        }
