# System Architecture (Hour 7)

```mermaid
flowchart TD
    UI[Browser UI: HTML/Tailwind/JS + Leaflet.js map]
    API[FastAPI REST layer]
    SVC[Service layer]
    ENGINE[Route engine: distance, nearest-neighbor, 2-opt]
    ORM[SQLAlchemy]
    DB[(SQLite)]

    UI -->|HTTP/JSON| API
    API --> SVC
    SVC --> ENGINE
    SVC --> ORM
    ENGINE --> ORM
    ORM --> DB
```

Same layering rationale as the previous project: the route engine is plain Python, independent of FastAPI, so every algorithm is unit-testable with pytest before any web layer exists.
