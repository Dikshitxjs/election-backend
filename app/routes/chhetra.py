from flask import Blueprint, jsonify

chhetra_bp = Blueprint("chhetra", __name__)

@chhetra_bp.route("/", methods=["GET"])
def get_chhetras():
    return jsonify([
        {"id": 1, "name": "Kathmandu-1"},
        {"id": 2, "name": "Kathmandu-2"},
        {"id": 3, "name": "Pokhara-3"},
    ])
