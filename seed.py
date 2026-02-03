from app import create_app
from app.database.db import db
from app.models.candidate import Candidate
from app.models.chhetra import Chhetra

def seed():
    app = create_app()

    with app.app_context():
        db.create_all()

        # --------------------
        # CHHETRAS (10 total)
        # --------------------
        chhetras = [
            {"id": 1, "name": "Jhapa-05", "region": "Province 1"},
            {"id": 2, "name": "Sarlahi-04", "region": "Province 2"},
            {"id": 3, "name": "Jhapa-02", "region": "Province 1"},
            {"id": 4, "name": "Bhaktapur-02", "region": "Bagmati"},
            {"id": 5, "name": "Chitwan-03", "region": "Bagmati"},
            {"id": 6, "name": "Tanahun-01", "region": "Gandaki"},
            {"id": 7, "name": "Kathmandu-03", "region": "Bagmati"},
            {"id": 8, "name": "Kathmandu-01", "region": "Bagmati"},
            {"id": 9, "name": "Gulmi-01", "region": "Lumbini"},
            {"id": 10, "name": "Rukum East", "region": "Lumbini"},
        ]

        chhetra_added = 0
        for ch in chhetras:
            if not Chhetra.query.filter_by(name=ch["name"]).first():
                db.session.add(Chhetra(**ch))
                chhetra_added += 1

        # --------------------
        # CANDIDATES (3 per chhetra)
        # Parties: UML, Congress, RSP
        # --------------------
        candidates = []
        for ch_id, ch in enumerate(chhetras, start=1):
            candidates.extend([
                {"name": f"Candidate {ch_id}-1", "party": "UML", "photo": None, "chhetra_id": ch_id},
                {"name": f"Candidate {ch_id}-2", "party": "Congress", "photo": None, "chhetra_id": ch_id},
                {"name": f"Candidate {ch_id}-3", "party": "RSP", "photo": None, "chhetra_id": ch_id},
            ])

        candidate_added = 0
        for c in candidates:
            exists = Candidate.query.filter_by(
                name=c["name"],
                chhetra_id=c["chhetra_id"]
            ).first()

            if not exists:
                db.session.add(Candidate(**c))
                candidate_added += 1

        if chhetra_added or candidate_added:
            db.session.commit()

        print(f" Chhetras added: {chhetra_added}")
        print(f" Candidates added: {candidate_added}")


if __name__ == "__main__":
    seed()
