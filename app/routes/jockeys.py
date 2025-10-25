from flask import Blueprint, jsonify
from marshmallow import ValidationError
from ..extensions import db
from ..models import Jockey, Entry
from ..schemas import JockeyCreateSchema, JockeySchema
from ..utils import get_json
from ..utils import roles_required

bp = Blueprint("jockeys", __name__)

@bp.post("")
@roles_required("admin","registrar")
def create_jockey():
    try:
        payload = JockeyCreateSchema().load(get_json())
    except (ValidationError, ValueError) as e:
        return {"error": str(e)}, 400

    jockey = Jockey(**payload)
    db.session.add(jockey)
    db.session.commit()
    return JockeySchema().dump(jockey), 201

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