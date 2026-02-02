from flask import Blueprint, jsonify, request, current_app

contact_bp = Blueprint("contact", __name__, strict_slashes=False)


@contact_bp.route("", methods=["GET"])
@contact_bp.route("/", methods=["GET"])
def get_contact():
    # Return only a helpful note for users — do not expose admin email/phone.
    note = current_app.config.get("CONTACT_NOTE") or "If you cannot find your chhetra number, please send us a message using the form and include your email so we can reply."
    return jsonify({"note": note})


@contact_bp.route("", methods=["POST"])
@contact_bp.route("/", methods=["POST"])
def post_contact():
    # Receiver for contact form. We require the user to include their email
    
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    message = data.get("message")
    user_email = data.get("email")

    # Validation: require message and user email
    if not message:
        return jsonify({"error": "Message is required"}), 400
    if not user_email:
        return jsonify({"error": "Your email is required so we can reply"}), 400

    # Log the incoming message server-side for later processing.
    snippet = (message[:200] + "...") if len(message) > 200 else message
    current_app.logger.info("Contact form received: %s", {"name": name, "email": user_email, "message": snippet})

    # TODO: 

    return jsonify({"status": "received"}), 201
