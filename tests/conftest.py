import pytest
from app import create_app, db as _db

TEST_DB = 'sqlite:///:memory:'

@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DB,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    ctx = app.app_context()
    ctx.push()
    _db.create_all()
    yield app
    _db.session.remove()
    _db.drop_all()
    ctx.pop()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return _db
