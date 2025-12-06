from flask import Flask

def test_get_json_success():
    from app.utils import get_json
    app = Flask(__name__)

    with app.test_request_context(json={"x": 123}):
        assert get_json()["x"] == 123

def test_get_json_error():
    from app.utils import get_json
    from werkzeug.exceptions import BadRequest
    from flask import Flask

    app = Flask(__name__)
    with app.test_request_context(data="not json"):
        try:
            get_json()
            assert False, "Expected exception"
        except BadRequest:
            assert True

def test_roles_required_decorator_allows():
    from app.utils import roles_required
    from flask import Flask

    app = Flask(__name__)
    app.config["TESTING"] = True  # пропускаем проверку JWT

    @roles_required("admin")
    def handler():
        return 1

    assert handler() == 1
