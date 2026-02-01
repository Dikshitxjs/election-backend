# Simple rate limit: user can only vote once
from app.database.db import db_session
from app.models.vote import Vote

def can_vote(user_id):
    """Check if the user has already voted"""
    vote = db_session.query(Vote).filter_by(user_id=user_id).first()
    return vote is None
# Simple rate limit: user can only vote once
from app.database.db import db_session
from app.models.vote import Vote

def can_vote(user_id):
    """Check if the user has already voted"""
    vote = db_session.query(Vote).filter_by(user_id=user_id).first()
    return vote is None
