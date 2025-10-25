from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields, validate, ValidationError
from ..extensions import db
from ..models import User, Role

bp = Blueprint("auth", __name__)

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(allow_none=True)
    roles = fields.List(fields.Str(), load_default=[])

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

@bp.post("/register")
def register():
    try:
        data = RegisterSchema().load(request.get_json())
    except ValidationError as e:
        return {"error": e.messages}, 400
    if User.query.filter_by(email=data["email"]).first():
        return {"error":"Email already in use"}, 400
    u = User(email=data["email"], full_name=data.get("full_name"))
    u.set_password(data["password"])
    for rname in data.get("roles", []):
        r = Role.query.filter_by(name=rname).first()
        if not r:
            r = Role(name=rname); db.session.add(r)
        u.roles.append(r)
    db.session.add(u); db.session.commit()
    return {"id": u.id, "email": u.email, "roles": [r.name for r in u.roles]}, 201

@bp.post("/login")
def login():
    try:
        data = LoginSchema().load(request.get_json())
    except ValidationError as e:
        return {"error": e.messages}, 400
    u = User.query.filter_by(email=data["email"]).first()
    if not u or not u.check_password(data["password"]):
        return {"error":"Invalid credentials"}, 401

    # <-- ВАЖНО: identity = строковый id, роли в additional_claims
    token = create_access_token(
        identity=str(u.id),
        additional_claims={"roles": [r.name for r in u.roles]}
    )
    return {"access_token": token}
