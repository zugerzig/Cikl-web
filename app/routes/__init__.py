from flask import Flask
from .horses import bp as horses_bp
from .jockeys import bp as jockeys_bp
from .events import bp as events_bp
from .results import bp as results_bp
from .auth import bp as auth_bp

def register_blueprints(app: Flask):
    app.register_blueprint(horses_bp, url_prefix="/api/horses")
    app.register_blueprint(jockeys_bp, url_prefix="/api/jockeys")
    app.register_blueprint(events_bp, url_prefix="/api/events")
    app.register_blueprint(results_bp, url_prefix="/api/results")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
