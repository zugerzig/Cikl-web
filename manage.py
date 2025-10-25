from app import create_app
from app.extensions import db
from app.models import Owner, Horse, Jockey, Event, Entry

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Owner": Owner,
        "Horse": Horse,
        "Jockey": Jockey,
        "Event": Event,
        "Entry": Entry,
    }
