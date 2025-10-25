from flask import Blueprint, jsonify
from marshmallow import ValidationError
from ..extensions import db
from ..models import Horse, Entry
from ..schemas import HorseCreateSchema, HorseSchema
from ..utils import get_json
from ..utils import roles_required

bp = Blueprint("horses", __name__)

@bp.post("")
@roles_required("admin","registrar")
def create_horse():
    try:
        payload = HorseCreateSchema().load(get_json())
    except (ValidationError, ValueError) as e:
        return {"error": str(e)}, 400

    horse = Horse(**payload)
    db.session.add(horse)
    db.session.commit()
    return HorseSchema().dump(horse), 201

@bp.get("/<int:horse_id>/events")
def horse_events(horse_id: int):
    entries = (
        db.session.query(Entry)
        .filter(Entry.horse_id == horse_id)
        .order_by(Entry.event_id)
        .all()
    )
    res = [
        {
            "event_id": e.event_id,
            "event_title": e.event.title,
            "venue": e.event.venue,
            "starts_at": e.event.starts_at.isoformat(),
            "jockey_id": e.jockey_id,
            "jockey_name": e.jockey.name,
            "place": e.place,
            "time_ms": e.time_ms,
        }
        for e in entries
    ]
    return jsonify(res)