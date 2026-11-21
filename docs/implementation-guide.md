# Route Optimizer: Implementation & Testing Guide (Hours 10-35)

Continues directly from `route-optimizer-planning-pack.md` (Hours 1–9). Everything below assumes the schema in §7, the pseudocode in §8, and the wireframes in §9 of that document are the source of truth. This guide is deliberately specification-level, not finished code: file names, function signatures, endpoint contracts, and exact test cases, so each hour has a clear target rather than an open-ended "build the thing" instruction.

---

## Phase: Core Engine (Hours 10–18)

The whole point of this phase is that the route engine works and is fully tested before FastAPI, SQLAlchemy, or the browser are involved in any of the logic. Everything here should be plain Python functions operating on lists of coordinates.

### Hour 10: Database setup

Create the venv, install `fastapi`, `uvicorn`, `sqlalchemy`, `pytest`. Build `app/database.py`: a SQLAlchemy engine pointed at a local SQLite file, a `SessionLocal`, and a declarative `Base`. Register a `sqlalchemy.event.listens_for(engine, "connect")` handler that runs `PRAGMA foreign_keys = ON` on every new connection. SQLite does not enforce foreign keys unless this is set explicitly on each connection, and it's a common, easy-to-miss gap that would quietly break SC1 and SC6 later.

Build a minimal `app/main.py` with a single `GET /health` endpoint that opens a DB session and closes it, just to confirm the whole chain (FastAPI, SQLAlchemy, SQLite file) actually connects.

**Deliverable:** `uvicorn app.main:app` boots, `/health` returns 200, the `.db` file exists on disk.

### Hour 11: Database models

Build `app/models.py` with `Stop`, `Route`, and `RouteStop`, matching §7 exactly: `stop_id`/`route_id`/`route_stop_id` primary keys, `input_order` and `optimized_order` (nullable) on `RouteStop`. Add two constraints while you're in here, since they're cheap now and expensive to retrofit: a unique constraint on `(route_id, stop_id)` so a stop can't be added to the same route twice, and a unique constraint on `(route_id, input_order)` so two stops can't claim the same position.

Write `tests/test_models.py` immediately: create a stop and a route, link them through `RouteStop`, query it back, and confirm that inserting a `RouteStop` with a nonexistent `stop_id` raises an `IntegrityError`. That last check is the actual proof that the Hour 10 PRAGMA setting is doing something.

**Deliverable:** tables created via `Base.metadata.create_all`, relationship and FK-rejection tests passing.

### Hour 12: Synthetic data

Build a fixtures module (`tests/conftest.py`) with three things: a random-stop generator parameterized by count and a bounding box (for later scaling tests), the exact six coordinates from §13's verified worked example, hardcoded, and one or two hand-built shapes (a square, a triangle) where the optimal tour is obvious by inspection. All three get reused constantly from here on, so it's worth getting this right once rather than re-deriving coordinates in every test file.

**Deliverable:** a fixtures module every later test hour imports from.

### Hour 13: Distance calculation

Build `app/engine/distance.py`:

```
def haversine_distance(a, b) -> float
def total_distance(ordered_stops) -> float
```

Implement exactly per §8.1–8.2. Before touching the worked example, sanity-check `haversine_distance` against one or two independently known real-world city-pair distances, since that validates the raw formula implementation separately from the routing algorithms that depend on it.

**Deliverable:** `tests/test_distance.py` passing against both the reference distances and the §13 pairwise table.

### Hour 14: Nearest-neighbor construction

Build `app/engine/nearest_neighbor.py`:

```
def nearest_neighbor(stops, depot_index=0) -> list
```

Test against the worked example: the result should match the Depot → E → B → D → C → A tour at 13.766 km. Also test the trivial cases now rather than deferring them: a depot with zero other stops, a depot with exactly one other stop, and a set containing two stops at identical coordinates (should complete without error, with a zero-length edge between them).

**Deliverable:** `tests/test_nearest_neighbor.py`, matched against §13's exact numbers.

### Hour 15: 2-opt improvement (naive, on purpose)

Build `app/engine/two_opt.py` using the naive version from §8.4 exactly as written, full `total_distance` recompute per candidate. Do not optimize yet. Test against the worked example: feeding it the Hour 14 NN result should produce the 12.657 km tour. Also test: an already-optimal small route (e.g. the square from Hour 12) should come back unchanged, and a 2-stop route should come back unchanged because no valid `(i, j)` pair exists once the depot is excluded from the swap range.

**Deliverable:** `tests/test_two_opt.py`, matched against §13.

### Hour 16: Route comparison

Build `app/engine/compare.py` per §8.5. Test using the worked example: naive = the Hour 14 NN tour, optimized = the Hour 15 2-opt tour, improvement should come out to roughly 8.1%.

**Deliverable:** `tests/test_compare.py`.

### Hour 17: Edge-case hardening

Go back through every edge case named in §8.5 and §10 as a deliberate checklist rather than trusting it's all covered incidentally: 0 stops, 1 stop, duplicate coordinates, already-optimal input. Decide now how the engine signals invalid input (a custom exception, e.g. `InvalidRouteError`, is cleaner than returning `None` and checking for it everywhere) since this decision determines how Hour 20's API layer converts engine failures into HTTP error responses.

**Deliverable:** a short table (edge case → expected behavior) that becomes the backbone of §10's testing strategy once real results replace the placeholders.

### Hour 18: Engine test suite, standalone

Run the full `app/engine/` test suite with zero dependency on FastAPI or SQLAlchemy, plain functions over plain coordinate lists. This is the same milestone as the old project's Hour 18: the actual computer science already works before a single web request has been handled.

**Deliverable:** a fully green test suite, worth a screenshot for later Criterion D evidence.

---

## Phase: Backend & Frontend (Hours 19–26)

### Hour 19: FastAPI foundation

Structure: `app/main.py`, `app/routers/`, `app/schemas/` (Pydantic), `app/services/` (the glue between routes, the DB, and the engine). Start with the simplest possible real endpoints, `GET /stops` and `GET /routes`, just to prove the full chain (FastAPI → `Depends(get_db)` → SQLAlchemy → SQLite) works before adding anything more complex.

**Deliverable:** FastAPI serving real DB-backed data, auto-docs visible at `/docs`.

### Hour 20: Stop/route CRUD

Endpoints:

```
POST   /stops
GET    /stops
GET    /stops/{id}
PUT    /stops/{id}
DELETE /stops/{id}

POST   /routes
GET    /routes
GET    /routes/{id}
PUT    /routes/{id}
DELETE /routes/{id}

POST   /routes/{route_id}/stops        (adds a stop, auto-assigns next input_order)
DELETE /routes/{route_id}/stops/{stop_id}
```

Pydantic schemas: `StopCreate`, `StopRead`, `RouteCreate`, `RouteRead` (with a nested list of stops). Enforce coordinate ranges (`latitude` between -90 and 90, `longitude` between -180 and 180) as Pydantic field validators rather than manual checks scattered through the endpoint bodies, this is a clean, declarative place for SC6's range rule to live.

**Deliverable:** full CRUD, tested with FastAPI's `TestClient` against both valid input and the invalid cases (bad ID, out-of-range coordinate, duplicate stop in one route).

### Hour 21: The optimize + compare endpoint

The centerpiece: `POST /routes/{route_id}/optimize`. It pulls the route's stops in `input_order`, runs `nearest_neighbor`, runs `two_opt`, writes `optimized_order` back to each `RouteStop` row, and returns:

```
{
  "naive_order": [stop_id, stop_id, ...],
  "optimized_order": [stop_id, stop_id, ...],
  "naive_distance_km": 13.77,
  "optimized_distance_km": 12.66,
  "improvement_percent": 8.1
}
```

Test it by seeding the DB with the §13 worked example's six stops through the real API, calling `/optimize`, and checking the response numbers match §13 within tolerance. This is the single test that proves the entire stack, not just the engine, produces the right answer.

**Deliverable:** one endpoint that exercises everything built so far, end to end.

### Hour 22: Frontend base + Leaflet

Static skeleton: `index.html`, Tailwind via CDN, a small `app.js`, Leaflet loaded via CDN over OpenStreetMap tiles. Get a pannable, zoomable map rendering and confirm click events report back a `(lat, lng)` pair before building anything on top of it.

**Deliverable:** a blank page with a working map.

### Hour 23: Stop entry + route builder

Wire the click-to-drop-a-pin flow to `POST /stops`. Build the route builder screen from §9: pick stops from a list, `POST /routes` to create the route, then `POST /routes/{id}/stops` for each selected stop in order.

**Deliverable:** stops and routes can be created entirely through the UI.

### Hour 24: Route view

The centerpiece screen from §9: call `POST /routes/{id}/optimize`, render both polylines (dashed for naive, solid for optimized), and show the stats panel with both distances and the improvement percentage.

**Deliverable:** the "watch the line get shorter" screen, working against real backend data.

### Hour 25: Frontend validation

Mirror the backend's rules on the frontend: disable "Add Stop" until a pin is actually dropped, and turn a failed API call's 422 response into a readable message instead of raw JSON. This is a second layer of the SC6 reliability story, not a replacement for the backend validation from Hour 20.

**Deliverable:** a data-entry flow a normal user can't easily break by accident.

### Hour 26: End-to-end integration

Walk every user flow start to finish in the actual browser: create several stops, build a route, optimize it, view naive vs. optimized, return to the route list, reopen the route, and confirm `optimized_order` persisted correctly. This is where frontend and backend assumptions that seemed fine in isolation usually turn out to disagree. Fix what breaks. After this hour, stop adding features.

**Deliverable:** the complete product, working end to end.

---

## Phase: Testing & Optimization (Hours 27–30)

### Hour 27: Reliability testing

Deliberately try to break it. Specific cases: a route with 0 stops, a route with 1 stop, adding a duplicate stop to the same route, a stop with `latitude = 200`, non-numeric coordinate input, deleting a stop that's still referenced by an existing route, calling `/optimize` on a route that was never given any stops.

**Deliverable:** an Input → Expected → Actual → Pass/Fail table, same format as the old project, every failure fixed before moving on.

### Hour 28: Correctness testing

Re-run the §13 worked example, but this time through the real API rather than calling engine functions directly: seed via `POST /stops` and `POST /routes`, call `/optimize`, check the response. This catches bugs that Hour 18's engine-only tests structurally couldn't, anything introduced in the service or API layer on the way from database rows to JSON response.

**Deliverable:** a correctness matrix (Expected / Actual / Difference / Pass-Fail), reusable directly in Criterion D and the final SC test matrix.

### Hour 29: Efficiency benchmarking

Generate stop sets at 10, 50, 100, and 500 using Hour 12's random generator. Time the `/optimize` call at each size with `time.perf_counter()`. Worth timing both the raw engine call and the full HTTP round trip separately, so you know whether any slowness is coming from the algorithm or from FastAPI/DB overhead.

**Deliverable:** a real benchmark table from your own machine, used to set SC5's actual target number instead of guessing at it in §3.

### Hour 30: Optimization

Implement both techniques from §8.4: the precomputed n×n distance matrix, and delta-based swap evaluation (compute only the four edges a candidate swap touches, rather than the whole route). Re-run Hour 29's exact benchmark script against the optimized version for a genuine before/after table, this is likely the strongest single Criterion D excerpt in the whole project. Then re-run the full §13 worked-example test suite against the optimized version too. It's an easy place to introduce a silent correctness bug (getting the four affected edges wrong), and the whole point of having the worked example is that a mistake here shows up immediately instead of hiding.

**Deliverable:** a before/after benchmark table, and confirmation that optimization didn't change correctness.

---

## Phase: Finalization (Hours 31–35)

### Hour 31: Final functionality pass

Run through the SC-mapped scenarios fresh, as if using it for the first time: create stops, build a 5+ stop route, optimize it, view naive vs. optimized, submit an invalid stop, run a 100+ stop route. Fix whatever surfaces. Freeze scope here.

**Deliverable:** a feature-complete, frozen product.

### Hour 32: Full SC1–SC7 test matrix

Pull together everything from Hours 18, 27, 28, and 29/30 into one final matrix mapping each success criterion to its actual test evidence and real pass/fail result, replacing every placeholder number in §3 and §10 with the real ones.

**Deliverable:** the master evidence document Criterion D and E both draw from.

### Hour 33: Criterion D evidence

Select and annotate the strongest excerpts. Given the roughly 1,000-word budget for 12 marks, priority order: the 2-opt delta optimization with its before/after benchmark (strongest single piece), nearest-neighbor construction, the depot-exclusion boundary logic in 2-opt, the FK/PRAGMA integrity setup, and one validation example. For each, the WHAT / WHY / HOW / ALTERNATIVE / RESULT structure from before still applies, and code excerpts get comments added at this stage even though the working repo stays comment-free.

**Deliverable:** a curated Criterion D draft.

### Hour 34: Video and evidence organization

Sequence: open the app, add several stops on the map, build a route, show the naive order, run optimize, show the optimized order and improvement percentage, submit an invalid stop and show it get rejected, run a 100+ stop route to show it completing quickly, briefly show the Hour 30 before/after benchmark numbers.

**Deliverable:** recorded demonstration, organized evidence folder.

### Hour 35: Evaluation and consistency audit

Build the SC-by-SC evidence table (met / partially met / not met, and why). Write Criterion E: genuine strengths, genuine weaknesses, and one or two specific, bounded future improvements, good candidates already exist from earlier hours (Or-opt moves or multiple NN restarts to escape local optima, from §8.4; multi-vehicle routing, from §2's out-of-scope list). Finish with the full A → B → C → D → E consistency check: does the final product actually answer the problem defined in Hour 1?

**Deliverable:** final evaluation, and a complete, internally consistent IA.
