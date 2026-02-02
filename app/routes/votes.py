from flask import Blueprint, request, jsonify
from app.database.db import db
from app.models.votes import Vote
from app.models.candidate import Candidate

votes_bp = Blueprint("votes", __name__)

# --- POST / GET votes ---
@votes_bp.route("/", methods=["GET", "POST"])
def votes():
    if request.method == "GET":
        # Optional: filter by candidateId
        candidate_id = request.args.get("candidateId", type=int)
        query = Vote.query
        if candidate_id:
            query = query.filter_by(candidate_id=candidate_id)

        votes_list = [{
            "id": v.id,
            "userId": v.user_id,
            "candidateId": v.candidate_id,
            "voteType": v.vote_type
        } for v in query.all()]
        return jsonify(votes_list)

    elif request.method == "POST":
        data = request.json or {}
        candidate_id = data.get("candidateId")
        vote_type = data.get("voteType")
        fingerprint = data.get("fingerprint")
        user_id = data.get("userId") or 0

        if fingerprint:
            try:
                user_id = abs(hash(fingerprint)) % (10 ** 12)
            except Exception:
                user_id = 0

        # Prevent duplicate votes for same candidate
        if user_id:
            existing = Vote.query.filter_by(user_id=user_id, candidate_id=candidate_id).first()
            if existing:
                if existing.vote_type == vote_type:
                    support = Vote.query.filter_by(candidate_id=candidate_id, vote_type="support").count()
                    oppose = Vote.query.filter_by(candidate_id=candidate_id, vote_type="oppose").count()
                    return jsonify({"supportCount": support, "opposeCount": oppose, "alreadyVoted": True})
                else:
                    try:
                        existing.vote_type = vote_type
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        return jsonify({"error": "Failed to update vote", "detail": str(e)}), 500

                    support = Vote.query.filter_by(candidate_id=candidate_id, vote_type="support").count()
                    oppose = Vote.query.filter_by(candidate_id=candidate_id, vote_type="oppose").count()
                    return jsonify({"supportCount": support, "opposeCount": oppose, "updated": True})

        # Record new vote (or anonymous)
        vote = Vote(user_id=user_id, candidate_id=candidate_id, vote_type=vote_type)
        try:
            db.session.add(vote)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to record vote", "detail": str(e)}), 500

        support = Vote.query.filter_by(candidate_id=candidate_id, vote_type="support").count()
        oppose = Vote.query.filter_by(candidate_id=candidate_id, vote_type="oppose").count()

        return jsonify({"supportCount": support, "opposeCount": oppose})

# --- GET /api/votes/stats ---
@votes_bp.route("/stats/", methods=["GET"])
def stats():
    try:
        votes = Vote.query.all()
        totals = {"support": 0, "oppose": 0}
        by_chhetra = {}

        for v in votes:
            if v.vote_type == "support":
                totals["support"] += 1
            else:
                totals["oppose"] += 1

            c = Candidate.query.get(v.candidate_id)
            ch = c.chhetra_id if c else 0
            ch_key = str(ch)
            if ch_key not in by_chhetra:
                by_chhetra[ch_key] = {"support": 0, "oppose": 0}
            if v.vote_type == "support":
                by_chhetra[ch_key]["support"] += 1
            else:
                by_chhetra[ch_key]["oppose"] += 1

        return jsonify({"totals": totals, "byChhetra": by_chhetra})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
