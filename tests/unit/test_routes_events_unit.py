from flask import Flask
from app.routes.events import create_event


def test_create_event_minimal(monkeypatch):
    app = Flask(__name__)
    app.config["TESTING"] = True

    # get_json → возвращает фиктивный payload
    monkeypatch.setattr("app.routes.events.get_json", lambda: {"name": "Ev1"})

    # подменяем SQLAlchemy session.add/commit
    class DummySession:
        def add(self, x): pass
        def commit(self): pass
    monkeypatch.setattr("app.routes.events.db.session", DummySession())

    with app.app_context():
        resp, status = create_event()
        assert status == 201
        assert resp["name"] == "Ev1"
        assert resp["venue"] == "Test Venue"
