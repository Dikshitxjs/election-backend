from app.database.db import db

class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    party = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=True)

    #  add ForeignKey
    chhetra_id = db.Column(db.Integer, db.ForeignKey("chhetras.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "party": self.party,
            "photo": self.photo,
            "chhetra_id": self.chhetra_id
        }
