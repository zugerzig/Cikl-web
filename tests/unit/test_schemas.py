import pytest
from marshmallow import ValidationError

def test_horse_create_schema_success():
    from app.schemas import HorseCreateSchema
    data = {"name": "Horse123"}
    out = HorseCreateSchema().load(data)
    assert out["name"] == "Horse123"

def test_horse_create_schema_fail():
    from app.schemas import HorseCreateSchema
    with pytest.raises(ValidationError):
        HorseCreateSchema().load({"name": ""})

def test_event_schema_minimal():
    from app.schemas import EventCreateSchema
    with pytest.raises(ValidationError):
        EventCreateSchema().load({"name": ""})

def test_entry_schema_success():
    from app.schemas import EntryCreateSchema
    data = {"event_id": 1, "horse_id": 2, "jockey_id": 3}
    out = EntryCreateSchema().load(data)
    assert out["horse_id"] == 2
