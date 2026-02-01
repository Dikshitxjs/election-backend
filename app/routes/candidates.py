from flask import Blueprint, jsonify
from app.models.candidate import Candidate
from app.models.votes import Vote
from app.models.comment import Comment

candidates_bp = Blueprint("candidates", __name__)

@candidates_bp.route("/", methods=["GET"])
def get_candidates():
    candidates = Candidate.query.all()
    result = []

    for c in candidates:
        support_count = Vote.query.filter_by(candidate_id=c.id, vote_type="support").count()
        oppose_count = Vote.query.filter_by(candidate_id=c.id, vote_type="oppose").count()
        comments = Comment.query.filter_by(candidate_id=c.id).order_by(Comment.id.desc()).limit(5).all()

        # frontend-relative photo/path so browser can load from frontend server's public/ folder
        photo_url = c.photo if c.photo else f"/candidates/{c.id}.svg"

        #  party badge path (try partyIcon field later if you add it to DB)
        party_slug = (c.party or "").lower().replace(" ", "-")
        party_icon = f"/party-badges/{party_slug}.svg"

        result.append({
            "id": c.id,
            "name": c.name,
            "party": c.party,
            "partyIcon": party_icon,
            "photo": photo_url,
            "chhetraId": c.chhetra_id,
            "supportCount": support_count,
            "opposeCount": oppose_count,
            "comments": [{"id": cm.id, "message": cm.message} for cm in comments],
        })

    return jsonify(result)
