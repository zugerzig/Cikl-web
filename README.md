# Races API (Flask + PostgreSQL)

## Запуск в Docker
```bash
cp .env.example .env
docker compose up --build
```
Откройте: http://localhost:5000/health → `{ "status": "ok" }`

## Запуск локально (venv)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# создайте БД races в локальном Postgres (или укажите свой DSN в .env)
flask db upgrade
flask run
```

## Эндпойнты (base: /api)
- POST /jockeys
- POST /horses
- POST /events
- POST /events/{event_id}/entries
- POST /results/{event_id}/{horse_id}/{jockey_id}
- GET  /events/{event_id}
- GET  /jockeys/{id}/events
- GET  /horses/{id}/events
