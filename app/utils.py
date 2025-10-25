from flask import request

def get_json():
    data = request.get_json(silent=True)
    if data is None:
        raise ValueError("Expected JSON body")
    return data


from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def roles_required(*required):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            roles = set(claims.get("roles", []))
            if not roles.intersection(required):
                return {"error": "forbidden", "required": list(required)}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
