from flask import Blueprint
from marshmallow import ValidationError
from ..extensions import db
from ..models import Entry
from ..schemas import ResultUpdateSchema
from ..utils import get_json
from ..utils import roles_required

bp = Blueprint("results", __name__)

@bp.post("/<int:event_id>/<int:horse_id>/<int:jockey_id>")
@roles_required("admin","judge")
def set_result(event_id: int, horse_id: int, jockey_id: int):
    entry = Entry.query.get_or_404((event_id, horse_id, jockey_id))
    try:
        payload = ResultUpdateSchema().load(get_json())
    except (ValidationError, ValueError) as e:
        return {"error": str(e)}, 400

    entry.place = payload["place"]
    entry.time_ms = payload["time_ms"]

    db.session.commit()
    return {
        "event_id": entry.event_id,
        "horse_id": entry.horse_id,
        "jockey_id": entry.jockey_id,
        "place": entry.place,
        "time_ms": entry.time_ms,
    }