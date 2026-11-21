# Technology Decisions (Hour 6)

| Layer | Choice | Alternative considered | Why |
|---|---|---|---|
| Database | SQLite | PostgreSQL | Relational integrity without server setup, already proven to work in an earlier build |
| ORM | SQLAlchemy | raw sqlite3 | Clear relationship management between Stop, Route, RouteStop |
| API | FastAPI | Flask | Typed validation, automatic docs |
| Frontend | HTML + Tailwind + JS + Leaflet.js | Google Maps JS API | Leaflet is free, open-source, needs no API key or billing account, and renders on free OpenStreetMap tiles. A real interactive map without derailing scope on API setup |
| Distance metric | Haversine (great-circle) formula | Real road-network routing API (OSRM/Google Directions) | Avoids an external dependency, rate limits, and cost. Straight-line distance is a standard, accepted simplification in introductory routing/TSP treatments at this scale |
| Testing | pytest | unittest | Same reasoning as before |

This table is direct Criterion D material once paired with what testing shows. "Chose Haversine over a routing API" is a stated choice. "Chose Haversine because it needs no external dependency and the error versus true road distance is negligible at city scale, which I confirmed against reference distances" is an evaluated one.
