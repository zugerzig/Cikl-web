from marshmallow import Schema, fields, validate

class OwnerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    address = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)

class HorseCreateSchema(Schema):
    name = fields.Str(required=True)
    sex = fields.Str(required=True, validate=validate.OneOf(["male", "female"]))
    birth_date = fields.Date(allow_none=True)
    owner_id = fields.Int(allow_none=True)

class HorseSchema(HorseCreateSchema):
    id = fields.Int(dump_only=True)

class JockeyCreateSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(allow_none=True)
    birth_date = fields.Date(allow_none=True)
    rating = fields.Float(load_default=0.0)

class JockeySchema(JockeyCreateSchema):
    id = fields.Int(dump_only=True)

class EventCreateSchema(Schema):
    title = fields.Str(allow_none=True)
    venue = fields.Str(required=True)
    starts_at = fields.DateTime(required=True)  # ISO 8601

class EventSchema(EventCreateSchema):
    id = fields.Int(dump_only=True)

class EntryCreateSchema(Schema):
    event_id = fields.Int(required=True)
    horse_id = fields.Int(required=True)
    jockey_id = fields.Int(required=True)

class ResultUpdateSchema(Schema):
    place = fields.Int(required=True, validate=validate.Range(min=1))
    time_ms = fields.Int(required=True, validate=validate.Range(min=0))
