from .candidates import candidates_bp
from .votes import votes_bp
from .comments import comments_bp
from .chhetra import chhetra_bp
from .contact import contact_bp

def register_routes(app):
    app.register_blueprint(candidates_bp, url_prefix="/api/candidates")
    app.register_blueprint(votes_bp, url_prefix="/api/votes")
    app.register_blueprint(comments_bp, url_prefix="/api/comments")
    app.register_blueprint(chhetra_bp, url_prefix="/api/chhetras")
    app.register_blueprint(contact_bp, url_prefix="/api/contact")

