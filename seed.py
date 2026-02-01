from app import create_app
from app.database.db import db
from app.models.candidate import Candidate


def seed():
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Insert specific candidates if missing. This avoids skipping when DB has any rows.
        samples = [
            # Chhetra 1 (3 members)
            {"name": "Asha Koirala", "party": "Party A", "photo": None, "chhetra_id": 1},
            {"name": "Ram Sharma", "party": "UML", "photo": None, "chhetra_id": 1},
            {"name": "Shyam Adhikari", "party": "RSP", "photo": None, "chhetra_id": 1},

            # Chhetra 2 (2 members)
            {"name": "Bikash Lama", "party": "Party B", "photo": None, "chhetra_id": 2},
            {"name": "Hari Singh", "party": "NC", "photo": None, "chhetra_id": 2},

            # Chhetra 3 (3 members)
            {"name": "Ram Kumar", "party": "Party C", "photo": None, "chhetra_id": 3},
            {"name": "Mina Thapa", "party": "Party D", "photo": None, "chhetra_id": 3},
            {"name": "Sita Gurung", "party": "Party E", "photo": None, "chhetra_id": 3},
        ]

        inserted = 0
        for s in samples:
            exists = Candidate.query.filter_by(name=s["name"]).first()
            if not exists:
                c = Candidate(name=s["name"], party=s["party"], photo=s["photo"], chhetra_id=s["chhetra_id"])
                db.session.add(c)
                inserted += 1

        if inserted > 0:
            db.session.commit()

        print(f"Inserted {inserted} new sample candidates")


if __name__ == "__main__":
    seed()
