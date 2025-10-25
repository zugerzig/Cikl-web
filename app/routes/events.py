from flask import Blueprint
from marshmallow import ValidationError
from ..extensions import db
from ..models import Event, Entry
from ..schemas import EventCreateSchema, EventSchema, EntryCreateSchema
from ..utils import get_json
from ..utils import roles_required

bp = Blueprint("events", __name__)

@bp.post("")
@roles_required("admin","registrar")
def create_event():
    try:
        payload = EventCreateSchema().load(get_json())
    except (ValidationError, ValueError) as e:
        return {"error": str(e)}, 400

    event = Event(**payload)
    db.session.add(event)
    db.session.commit()
    return EventSchema().dump(event), 201

@bp.post("/<int:event_id>/entries")
@roles_required("admin","registrar")
def add_entry(event_id: int):
    try:
        payload = EntryCreateSchema().load(get_json())
    except (ValidationError, ValueError) as e:
        return {"error": str(e)}, 400

    if payload["event_id"] != event_id:
        return {"error": "event_id mismatch"}, 400

    entry = Entry(**payload)
    db.session.add(entry)
    try:
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        return {"error": str(ex)}, 400

    return {
        "event_id": entry.event_id,
        "horse_id": entry.horse_id,
        "jockey_id": entry.jockey_id,
    }, 201

@bp.get("/<int:event_id>")
def get_event(event_id: int):
    event = Event.query.get_or_404(event_id)
    entries = (
        Entry.query.filter_by(event_id=event_id)
        .join(Entry.horse)
        .join(Entry.jockey)
        .order_by(Entry.place.is_(None), Entry.place.asc())
        .all()
    )
    return {
        "id": event.id,
        "title": event.title,
        "venue": event.venue,
        "starts_at": event.starts_at.isoformat(),
        "participants": [
            {
                "horse_id": e.horse_id,
                "horse_name": e.horse.name,
                "jockey_id": e.jockey_id,
                "jockey_name": e.jockey.name,
                "place": e.place,
                "time_ms": e.time_ms,
            }
            for e in entries
        ],
    }