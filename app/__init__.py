from flask import Flask
from typing import Union, Dict, Any, Type
from .config import Config
from .extensions import db, migrate
from .routes import register_blueprints


def create_app(config_object: Union[Type[Config], Dict[str, Any], None] = None) -> Flask:
    app = Flask(__name__)

    # --- ВАЖНО: поддержка dict для тестов ---
    if isinstance(config_object, dict):
        app.config.from_mapping(config_object)
    else:
        app.config.from_object(config_object or Config())

    # JSON настройки
    app.config["JSON_AS_ASCII"] = False
    app.json.ensure_ascii = False

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    from .extensions import jwt
    app.config["JWT_SECRET_KEY"] = app.config.get("SECRET_KEY", "dev")
    jwt.init_app(app)

    # Регистрация blueprints
    register_blueprints(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.after_request
    def force_utf8_json(resp):
        if resp.mimetype == "application/json":
            resp.headers["Content-Type"] = "application/json; charset=utf-8"
        return resp

    return app
