import os
from app import app
from app.database.db import db
from app.models.chhetra import Chhetra
from app.models.candidate import Candidate

def seed():
    with app.app_context():
        # Drop all tables first (safe reset)
        db.drop_all()
        db.create_all()
        print("✅ Database reset and tables created.")

        # --------------------
        # Chhetras
        # --------------------
        chhetras_data = [
            {"name": "Jhapa-05", "region": "Province 1"},
            {"name": "Sarlahi-04", "region": "Province 2"},
            {"name": "Jhapa-02", "region": "Province 1"},
            {"name": "Bhaktapur-02", "region": "Bagmati"},
            {"name": "Chitwan-03", "region": "Bagmati"},
            {"name": "Tanahun-01", "region": "Gandaki"},
            {"name": "Kathmandu-03", "region": "Bagmati"},
            {"name": "Kathmandu-01", "region": "Bagmati"},
            {"name": "Gulmi-01", "region": "Lumbini"},
            {"name": "Rukum East", "region": "Lumbini"},
        ]

        chhetras = []
        for ch_data in chhetras_data:
            ch = Chhetra(**ch_data)
            db.session.add(ch)
            chhetras.append(ch)
        db.session.commit()
        print(f"✅ Chhetras added: {len(chhetras)}")

        # --------------------
        # Candidates (3 per chhetra)
        # --------------------
        candidates = []
        for idx, ch in enumerate(chhetras, start=1):
            candidates.extend([
                Candidate(name=f"Candidate {idx}-1", party="UML", photo=None, chhetra_id=ch.id),
                Candidate(name=f"Candidate {idx}-2", party="Congress", photo=None, chhetra_id=ch.id),
                Candidate(name=f"Candidate {idx}-3", party="RSP", photo=None, chhetra_id=ch.id),
            ])

        db.session.add_all(candidates)
        db.session.commit()
        print(f"✅ Candidates added: {len(candidates)}")

if __name__ == "__main__":
    seed()
