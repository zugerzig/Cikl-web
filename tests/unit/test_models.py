def test_horse_model_repr():
    from app.models import Horse
    h = Horse(name="Thunder")
    assert h.name == "Thunder"

def test_event_defaults():
    from app.models import Event
    ev = Event(name="E1", title="T1", venue="V1")
    assert ev.name == "E1"
    assert ev.title == "T1"
    assert ev.venue == "V1"

def test_entry_links():
    from app.models import Entry, Event, Horse, Jockey
    ev = Event(id=1, name="E1", title="T1", venue="V1")
    ho = Horse(id=10, name="H1")
    jo = Jockey(id=20, name="J1")

    e = Entry(event_id=1, horse_id=10, jockey_id=20)

    assert e.event_id == ev.id
    assert e.horse_id == ho.id
    assert e.jockey_id == jo.id
