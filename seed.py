import os
from app import app
from app.database.db import db
from app.models.chhetra import Chhetra
from app.models.candidate import Candidate

DUMMY_FIRST = [
    "Anil", "Bikash", "Dipesh", "Kiran", "Milan",
    "Nabin", "Prakash", "Ramesh", "Suman", "Yogesh"
]

DUMMY_LAST = [
    "Adhikari", "Basnet", "Gurung", "Karki", "Poudel",
    "Rai", "Shrestha", "Tamang", "Thapa", "Magar"
]

GENUINE = {
    "Jhapa-05": [
        {"name": "Balen Shan", "party": "RSP"},
        {"name": "KP Oli", "party": "UML"},
        {"name": "Sagar Tamang", "party": "Congress"},
    ],
    "Kathmandu-03": [
        {"name": "Rameshwor Phuyal", "party": "UML"},
        {"name": "Rajy Pander", "party": "RSP"},
        {"name": "Ramesh Setu", "party": "Congress"},
    ],
    "Gulmi-01": [
        {"name": "Sagar Dhakal", "party": "RSP"},
    ],
    "Bhaktapur-02": [
        {"name": "Mahesh Basnet", "party": "UML"},
        {"name": "Rajiv Khatri", "party": "RSP"},
    ],
}

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
        
        # --------------------
        # Update candidate names with genuine + dummy data
        # --------------------
        professionalize_candidates()

def professionalize_candidates():
    """Update candidate names after seeding"""
    chhetra_map = {
        c.id: c.name
        for c in Chhetra.query.all()
    }

    dummy_i = 0
    dummy_j = 0

    candidates = Candidate.query.order_by(
        Candidate.chhetra_id,
        Candidate.id
    ).all()

    per_chhetra_index = {}

    for c in candidates:
        ch_name = chhetra_map.get(c.chhetra_id, "Unknown Region")

        if ch_name not in per_chhetra_index:
            per_chhetra_index[ch_name] = 0

        idx = per_chhetra_index[ch_name]
        genuine_list = GENUINE.get(ch_name, [])

        matched = False

        for g in genuine_list:
            if g["party"] == c.party and idx < len(genuine_list):
                c.name = g["name"]
                matched = True
                break

        if not matched:
            c.name = f"{DUMMY_FIRST[dummy_i]} {DUMMY_LAST[dummy_j]}"
            dummy_i = (dummy_i + 1) % len(DUMMY_FIRST)
            dummy_j = (dummy_j + 1) % len(DUMMY_LAST)

        per_chhetra_index[ch_name] += 1

    db.session.commit()
    print(f"✅ Updated {len(candidates)} candidates with genuine + dummy names")

if __name__ == "__main__":
    seed()
