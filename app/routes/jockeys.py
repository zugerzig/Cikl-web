from flask import Blueprint, jsonify, current_app
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models import Jockey, Entry
from ..schemas import JockeyCreateSchema, JockeySchema
from ..utils import get_json, roles_required

bp = Blueprint("jockeys", __name__)


# ====== Декоратор, отключающий авторизацию в тестовом режиме ======
def optional_roles_required(*roles):
    """
    Если включён TESTING → пропускаем авторизацию
    Иначе → применяем roles_required как обычно
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            # Тестовый режим → пропускаем auth
            if current_app.config.get("DISABLE_AUTH"):
                return f(*args, **kwargs)

            # Прод → требуем JWT и роли
            return roles_required(*roles)(f)(*args, **kwargs)

        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


# ================== POST /api/jockeys ==================
@bp.post("")
@optional_roles_required("admin", "registrar")
def create_jockey():
    try:
        payload = JockeyCreateSchema().load(get_json())
    except (ValidationError, ValueError) as e:
        return {"error": str(e)}, 400

    jockey = Jockey(**payload)
    db.session.add(jockey)
    db.session.commit()

    return JockeySchema().dump(jockey), 201


# ================== GET /api/jockeys/<id>/events ==================
@bp.get("/<int:jockey_id>/events")
def jockey_events(jockey_id: int):
    entries = (
        Entry.query.filter_by(jockey_id=jockey_id)
        .join(Entry.event)
        .order_by(Entry.event_id)
        .all()
    )

    res = [
        {
            "event_id": e.event_id,
            "event_title": e.event.title,
            "venue": e.event.venue,
            "starts_at": e.event.starts_at.isoformat(),
            "horse_id": e.horse_id,
            "horse_name": e.horse.name,
            "place": e.place,
            "time_ms": e.time_ms,
        }
        for e in entries
    ]

    return jsonify(res)
