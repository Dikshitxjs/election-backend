from flask import Blueprint, request, jsonify
from app.database.db import db
from app.models.comment import Comment

comments_bp = Blueprint("comments", __name__)

# --- GET + POST /api/comments/ ---
@comments_bp.route("/", methods=["GET", "POST"])
def comments():
    if request.method == "GET":
        # Optional query param to filter by candidate
        candidate_id = request.args.get("candidateId", type=int)
        fingerprint = request.args.get("fingerprint")
        query = Comment.query
        if candidate_id:
            query = query.filter_by(candidate_id=candidate_id)

        # If a fingerprint is provided, map it to a deterministic user_id
        # (same approach as votes endpoint) and filter by that user.
        if fingerprint:
            try:
                user_id = abs(hash(fingerprint)) % (10 ** 12)
                query = query.filter_by(user_id=user_id)
            except Exception:
                pass

        comments_list = [
            {"id": c.id, "userId": c.user_id, "candidateId": c.candidate_id, "message": c.message}
            for c in query.order_by(Comment.id.desc()).all()
        ]
        return jsonify(comments_list)

    elif request.method == "POST":
        data = request.json or {}
        user_id = data.get("userId") or 0
        fingerprint = data.get("fingerprint")
        candidate_id = data.get("candidateId")
        message = data.get("message", "")

        # If a fingerprint is provided, compute the same user_id mapping
        if fingerprint:
            try:
                user_id = abs(hash(fingerprint)) % (10 ** 12)
            except Exception:
                user_id = user_id or 0

        if not candidate_id or not message.strip():
            return jsonify({"error": "candidateId and message are required"}), 400

        comment = Comment(user_id=user_id, candidate_id=candidate_id, message=message)
        try:
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to save comment", "detail": str(e)}), 500

        # Return updated list of comments for that candidate
        comments_list = Comment.query.filter_by(candidate_id=candidate_id)\
            .order_by(Comment.id.desc()).all()
        return jsonify({
            "comments": [{"id": c.id, "userId": c.user_id, "message": c.message} for c in comments_list]
        })
