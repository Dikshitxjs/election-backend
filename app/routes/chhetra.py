from flask import Blueprint, jsonify
from app.models.chhetra import Chhetra
from app.models.candidate import Candidate

chhetra_bp = Blueprint("chhetra", __name__)

@chhetra_bp.route("/", methods=["GET"])
def get_chhetras():
    """Get all chhetras with candidate count"""
    chhetras = Chhetra.query.all()
    result = []
    
    for ch in chhetras:
        candidate_count = Candidate.query.filter_by(chhetra_id=ch.id).count()
        result.append({
            "id": ch.id,
            "name": ch.name,
            "region": ch.region,
            "candidateCount": candidate_count
        })
    
    return jsonify(result)

@chhetra_bp.route("/<int:chhetra_id>", methods=["GET"])
def get_chhetra(chhetra_id):
    """Get specific chhetra details"""
    chhetra = Chhetra.query.get(chhetra_id)
    
    if not chhetra:
        return jsonify({"error": "Chhetra not found"}), 404
    
    candidate_count = Candidate.query.filter_by(chhetra_id=chhetra.id).count()
    
    return jsonify({
        "id": chhetra.id,
        "name": chhetra.name,
        "region": chhetra.region,
        "candidateCount": candidate_count
    })

@chhetra_bp.route("/<int:chhetra_id>/candidates", methods=["GET"])
def get_chhetra_candidates(chhetra_id):
    """Get all candidates in a specific chhetra"""
    from app.models.votes import Vote
    from app.models.comment import Comment
    
    chhetra = Chhetra.query.get(chhetra_id)
    
    if not chhetra:
        return jsonify({"error": "Chhetra not found"}), 404
    
    candidates = Candidate.query.filter_by(chhetra_id=chhetra_id).all()
    result = []
    
    for c in candidates:
        support_count = Vote.query.filter_by(candidate_id=c.id, vote_type="support").count()
        oppose_count = Vote.query.filter_by(candidate_id=c.id, vote_type="oppose").count()
        comments = Comment.query.filter_by(candidate_id=c.id).order_by(Comment.id.desc()).limit(5).all()
        
        photo_url = c.photo if c.photo else f"/candidates/{c.id}.svg"
        party_slug = (c.party or "").lower().replace(" ", "-")
        party_icon = f"/party-badges/{party_slug}.svg"
        
        result.append({
            "id": c.id,
            "name": c.name,
            "party": c.party,
            "partyIcon": party_icon,
            "photo": photo_url,
            "chhetra_id": c.chhetra_id,
            "chhetraId": c.chhetra_id,
            "supportCount": support_count,
            "opposeCount": oppose_count,
            "comments": [{"id": cm.id, "message": cm.message} for cm in comments],
        })
    
    return jsonify(result)
