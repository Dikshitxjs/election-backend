import os
from app import app
from app.database.db import db
from app.models.chhetra import Chhetra
from app.models.candidate import Candidate

# Party short name to full name mapping
PARTY_NAMES = {
    "UML": "CPN (UML)",
    "Congress": "Nepali Congress",
    "RSP": "Rastriya Swatantra Party",
    "Maoist": "CPN (Maoist Centre)",
    "PLP": "Pragatisheel Loktantrik Party",
    "RPP": "Rastriya Prajatantra Party",
    "IND": "Independent",
    "ULP": "Unified Left Party",  # Assuming this exists based on seed data
}

GENUINE = {
    "Rukum East": [
        {"name": "Prachanda", "party": "Maoist"},
        {"name": "Sandeep Pun", "party": "PLP"},
    ],
    "Tanahun-01": [
        {"name": "Swornim Wagle", "party": "RSP"},
        {"name": "Govinda KC", "party": "Congress"},
    ],
    "Kathmandu-01": [
        {"name": "Rabindra Mishra", "party": "RPP"},
    ],
    "Kathmandu-03": [
        {"name": "Kulman Ghising", "party": "ULP"},
        {"name": "Raju Pandey", "party": "RSP"},
        {"name": "Rameshwor Phuyal", "party": "UML"},
        {"name": "Ramesh Aryal", "party": "Congress"},
    ],
    "Gulmi-01": [
        {"name": "Sagar Dhakal", "party": "RSP"},
        {"name": "Pradeep Gyawali", "party": "UML"},
        {"name": "Chandra Bhandari", "party": "Congress"},
    ],
    "Chitwan-03": [
        {"name": "Sabita Gautam", "party": "RSP"},
        {"name": "Renu Dhakal", "party": "Maoist"},
    ],
    "Bhaktapur-02": [
        {"name": "Mahesh Basnet", "party": "UML"},
        {"name": "Rajiv Khatri", "party": "RSP"},
        {"name": "Shova Pathak", "party": "IND"},
    ],
    "Jhapa-02": [
        {"name": "Devraj Ghimre", "party": "UML"},
        {"name": "Dibya Rana", "party": "RSP"},
    ],
    "Sarlahi-04": [
        {"name": "Amresh Singh", "party": "RSP"},
        {"name": "Ganagna Thapa", "party": "Congress"},
    ],
    "Jhapa-05": [
        {"name": "Balen Shan", "party": "RSP"},
        {"name": "KP Oli", "party": "UML"},
        {"name": "Sagar Tamang", "party": "Congress"},
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
        # Candidates (ONLY genuine candidates - no fallback)
        # --------------------
        candidates = []
        total_candidates = 0
        
        for ch in chhetras:
            genuine_list = GENUINE.get(ch.name, [])
            if genuine_list:
                for g in genuine_list:
                    candidates.append(
                        Candidate(
                            name=g.get("name"),
                            party=PARTY_NAMES.get(g.get("party"), g.get("party")),
                            photo=None,
                            chhetra_id=ch.id
                        )
                    )
                    total_candidates += 1
                print(f"   ✓ {ch.name}: {len(genuine_list)} genuine candidates added")
            else:
                print(f"   ⚠ {ch.name}: No genuine candidates (skipped)")

        db.session.add_all(candidates)
        db.session.commit()
        print(f"✅ Total candidates added: {total_candidates}")

if __name__ == "__main__":
    seed()
