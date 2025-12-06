from flask import Flask
from app.routes.horses import create_horse


def test_create_horse_success(monkeypatch):
    app = Flask(__name__)
    app.config["TESTING"] = True

    monkeypatch.setattr("app.routes.horses.get_json", lambda: {"name": "H1"})

    class DummySession:
        def add(self, x): pass
        def commit(self): pass
    monkeypatch.setattr("app.routes.horses.db.session", DummySession())

    with app.app_context():
        resp, status = create_horse()
        assert status == 201
        assert resp["name"] == "H1"
