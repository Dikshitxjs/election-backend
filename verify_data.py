#!/usr/bin/env python
"""Quick script to verify seeded data"""

from app import app
from app.models.candidate import Candidate
from app.models.chhetra import Chhetra

with app.app_context():
    candidates = Candidate.query.all()
    print(f'\n{"="*60}')
    print(f'Total candidates: {len(candidates)}')
    print(f'{"="*60}\n')
    
    chhetras = Chhetra.query.all()
    for ch in chhetras:
        ch_candidates = Candidate.query.filter_by(chhetra_id=ch.id).all()
        print(f'\n{ch.name} ({ch.region}): {len(ch_candidates)} candidates')
        print('-' * 50)
        for c in ch_candidates:
            print(f'  ✓ {c.name:25} | {c.party}')
    
    print(f'\n{"="*60}')
    print('✅ Data verification complete!')
    print(f'{"="*60}\n')
