from datetime import datetime
from app.database.db import db

class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    candidate_id = db.Column(db.Integer, nullable=False)
    vote_type = db.Column(db.String, nullable=False)  # "support" or "oppose"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "candidate_id": self.candidate_id,
            "vote_type": self.vote_type,
            "timestamp": self.timestamp.isoformat()
        }
