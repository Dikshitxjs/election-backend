from flask import Blueprint, request, jsonify
from app.database.db import db
from app.models.comment import Comment

comments_bp = Blueprint("comments", __name__)

@comments_bp.route("/", methods=["POST"])
def post_comment():
    data = request.json or {}

    # Support anonymous comments: if no userId provided, use 0
    user_id = data.get("userId") or 0

    comment = Comment(
        user_id=user_id,
        candidate_id=data.get("candidateId"),
        message=data.get("message", "")
    )

    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to save comment", "detail": str(e)}), 500

    comments = Comment.query.filter_by(candidate_id=data.get("candidateId"))\
        .order_by(Comment.id.desc()).all()

    return jsonify({
        "comments": [{"id": c.id, "message": c.message} for c in comments]
    })
