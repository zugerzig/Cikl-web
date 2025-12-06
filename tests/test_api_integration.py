def test_healthcheck(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get('status') == 'ok'

def test_create_jockey_and_get_events(client, db):
    payload = {"name": "Test Jockey"}
    rv = client.post('/api/jockeys', json=payload)
    assert rv.status_code in (200, 201)
    data = rv.get_json()
    jockey_id = data.get('id') or data.get('ID') or data.get('pk')
    assert jockey_id is not None

    rv = client.post('/api/events', json={"name": "Ev1"})
    assert rv.status_code in (200, 201)
    event_id = rv.get_json().get('id')
    assert event_id is not None

    rv = client.get(f'/api/jockeys/{jockey_id}/events')
    assert rv.status_code == 200

def test_create_horse_and_entry_and_result_flow(client):
    rv = client.post('/api/horses', json={"name": "Horse1"})
    assert rv.status_code in (200,201)
    horse = rv.get_json()
    hid = horse.get('id')

    rv = client.post('/api/jockeys', json={"name": "Jock1"})
    assert rv.status_code in (200,201)
    j = rv.get_json()
    jid = j.get('id')

    rv = client.post('/api/events', json={"name": "EventA"})
    assert rv.status_code in (200,201)
    ev = rv.get_json()
    eid = ev.get('id')

    rv = client.post(f'/api/events/{eid}/entries', json={"horse_id": hid, "jockey_id": jid})
    assert rv.status_code in (200,201)

    rv = client.post(f'/api/results/{eid}/{hid}/{jid}')
    assert rv.status_code < 400
