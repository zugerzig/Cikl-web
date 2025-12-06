from functools import wraps
from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def roles_required(*required):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            # ============================
            #  TEST MODE — NO AUTH CHECKS
            # ============================
            if current_app.config.get("TESTING", False):
                return fn(*args, **kwargs)

            # ============================
            #  NORMAL MODE — FULL CHECK
            # ============================
            verify_jwt_in_request()
            claims = get_jwt()
            roles = set(claims.get("roles", []))
            if not roles.intersection(required):
                return {"error": "forbidden", "required": list(required)}, 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
