from app import app
from app.database.db import db
from app.models.candidate import Candidate
from app.models.chhetra import Chhetra

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

def run():
    with app.app_context():
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
                c.name = f"{DUMMY_FIRST[dummy_i]} {DUMMY_LAST[dummy_j]} – {ch_name}"
                dummy_i = (dummy_i + 1) % len(DUMMY_FIRST)
                dummy_j = (dummy_j + 1) % len(DUMMY_LAST)

            per_chhetra_index[ch_name] += 1

        db.session.commit()
        print(f"Updated {len(candidates)} candidates (genuine + dummy)")

if __name__ == "__main__":
    run()
