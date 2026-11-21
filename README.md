# Route Optimizer

IB Computer Science Internal Assessment, Computational Solution (first assessment May 2027).

## What this is

A route optimization web application for Jimothy (fictional client, teacher-approved), a small delivery and errand operator who currently orders his daily stops by guesswork. The system builds an initial route with a nearest-neighbor algorithm, improves it with 2-opt local search, and shows the improvement against the naive order, both numerically and on a map.

## Tech stack

- Python, FastAPI, SQLAlchemy, SQLite
- Tailwind CSS, Leaflet.js
- pytest, managed with uv

## Running it

```
uv sync
uv run python -m scripts.seed_worked_example
uv run uvicorn app.main:app --reload
uv run pytest
```

The API docs are at http://127.0.0.1:8000/docs once the server is running.

## Project structure

```
route-optimizer/
├── app/
│   ├── engine/           pure Python route engine (distance, nearest-neighbor, 2-opt, comparison)
│   ├── routers/          FastAPI routers
│   ├── schemas/          Pydantic response models
│   ├── services/         database queries between routers and models
│   ├── database.py       engine, session, foreign key enforcement
│   ├── models.py         Stop, Route, RouteStop
│   └── main.py           app setup and /health
├── tests/                pytest suite
├── scripts/              seed data, isolated engine test run, mutation check
├── data/                 synthetic stop sets (reserved)
├── docs/                 planning and design documentation
│   ├── algorithms/       pseudocode and the verified worked example
│   └── wireframes/       UI screen designs
├── screenshots/          evidence for Criterion D and E
├── notes/
│   ├── development-log.md
│   └── ai-citation-log.md
└── README.md
```

## Status

Hours 1-9 (problem definition through UI design) are complete, see `docs/`. Hours 10-19 are built: database, models, the route engine with its test suite, and the read-only API. Hour 20 (stop and route CRUD endpoints) is next. Full hour-by-hour plan in `docs/35-hour-master-plan.md`.
