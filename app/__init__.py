from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .routes import register_blueprints


def create_app(config_object=None) -> Flask:
    app = Flask(__name__)

    # --- Загружаем конфигурацию ---
    if isinstance(config_object, dict):
        app.config.update(config_object)
    else:
        app.config.from_object(config_object or Config())

    # Настройки JSON
    app.config["JSON_AS_ASCII"] = False
    app.json.ensure_ascii = False

    # --- Инициализация расширений ---
    db.init_app(app)
    migrate.init_app(app, db)

    # JWT
    app.config["JWT_SECRET_KEY"] = app.config.get("SECRET_KEY", "dev")
    jwt.init_app(app)

    # --- Отключаем авторизацию в тестовой среде ---
    # Это позволит тестам выполнять POST /api/... без токена
    if app.config.get("TESTING"):
        app.config["DISABLE_AUTH"] = True

    # --- Регистрация всех маршрутов ---
    register_blueprints(app)

    # --- Health-check endpoint ---
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # --- Принудительное указание charset=utf-8 ---
    @app.after_request
    def force_utf8_json(resp):
        if resp.mimetype == "application/json":
            resp.headers["Content-Type"] = "application/json; charset=utf-8"
        return resp

    return app
