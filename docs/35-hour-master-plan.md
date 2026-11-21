# Route Optimizer: 35-Hour Master Plan

IB Computer Science Internal Assessment, Computational Solution (first assessment May 2027)

This is the single, start-to-finish walkthrough of all 35 hours. It pulls together `route-optimizer-planning-pack.md` (full diagrams, schemas, and pseudocode for Hours 1–9), `research-log.md` (Hour 2's sources), and `route-optimizer-implementation-guide.md` (full file/endpoint/test specifications for Hours 10–35) into one narrative. Those three documents are still the place to go for the actual mermaid diagrams, full pseudocode, and exact test tables. This one is for reading the whole plan in one sitting and checking where you are.

---

## Quick Reference

| Hour | Phase | Deliverable |
|---|---|---|
| 1 | Problem | Problem definition |
| 2 | Research | TSP heuristics, nearest-neighbor, 2-opt, Haversine, research log |
| 3 | Requirements | Requirements list, locked scope |
| 4 | Success criteria | SC1–SC7, locked |
| 5 | Planning | Decomposition |
| 6 | Research/architecture | Technology decisions |
| 7 | System design | Architecture + database design |
| 8 | Algorithm design | Pseudocode + verified worked example |
| 9 | UI design | Wireframes |
| 10 | Database setup | SQLite + SQLAlchemy configured |
| 11 | Database | Stop/Route/RouteStop models + relationships |
| 12 | Data | Synthetic stop sets, incl. controlled known-optimal sets |
| 13 | Core algorithm | Distance calculation + total route distance |
| 14 | Core algorithm | Nearest-neighbor construction |
| 15 | Core algorithm | 2-opt improvement (naive) |
| 16 | Core algorithm | Route comparison (naive vs optimized) |
| 17 | Polish | Edge-case handling across the engine |
| 18 | Testing | Unit-test the route engine independently of any web layer |
| 19 | Backend | FastAPI foundation |
| 20 | API | Stop/route CRUD endpoints |
| 21 | API | Optimize + compare endpoint |
| 22 | Frontend | Base UI + Leaflet map integration |
| 23 | Frontend | Stop entry (map click) + route builder |
| 24 | Frontend | Route view: naive/optimized toggle + stats panel |
| 25 | Frontend | Validation on the data-entry side |
| 26 | Integration | Connect everything end-to-end |
| 27 | Reliability | Edge-case/invalid-input testing |
| 28 | Correctness | Independent verification of distance/NN/2-opt output |
| 29 | Efficiency | Benchmark across stop counts (10/50/100/500) |
| 30 | Optimization | Precomputed distance matrix + delta-based swap, before/after benchmark |
| 31 | Final functionality | Feature-complete pass |
| 32 | Final testing | Full SC1–SC7 test matrix |
| 33 | Documentation | Criterion D evidence |
| 34 | Video | Demonstration + evidence organization |
| 35 | Finalization | Evaluation + IA consistency audit |

---

## Phase 1: Problem, Research & Design (Hours 1–9)

### Hour 1: Problem definition

Pin down exactly who has the problem and what the computer needs to do, no code yet. Jimothy (fictional client) runs a small delivery and errand service, visiting a list of stops each day in whatever order he remembers or received requests in. As the stop count grows, working out a genuinely good order by hand becomes infeasible, since the number of possible orderings grows factorially, and there's no way to know how much better a smarter order would be. The system needs to store stops and their locations, calculate distances between them, construct a reasonable initial visiting order automatically, improve that order algorithmically, and show the improvement, both numerically and visually, against the naive order.

**Deliverable:** problem definition written up (full text in planning pack §1).

### Hour 2: Research

Ground every algorithmic choice in an established, citable source instead of inventing anything from scratch. Researched: nearest-neighbor construction, 2-opt local search (including its 1958 origin and the rule that the fixed depot must be excluded from the swappable range), the delta-based swap-evaluation optimization, and the Haversine formula. Every choice in this project traces back to a named, standard technique, not an empirical guess, which is the direct fix for how research worked on the previous project.

**Deliverable:** research log, six sourced entries.

### Hour 3: Requirements

Translate the problem into a concrete requirements list, and just as importantly, an explicit out-of-scope list. Eleven essential requirements: store and retrieve stops and routes, modify and delete them safely, calculate pairwise and total route distance, construct an initial route (nearest-neighbor), improve it (2-opt), compare naive against optimized, visualize on a map, and handle a realistic stop count efficiently. Supporting requirements cover input validation, trivial-case handling, and clear error messages. Explicitly out of scope, with reasons: real-time traffic and live GPS, exact TSP solving, multi-vehicle routing, real road-network distance APIs, and authentication.

**Deliverable:** requirements list, full detail in planning pack §2.

### Hour 4: Success criteria

Lock measurable, testable criteria that every later hour refers back to. SC1 covers CRUD integrity for stops and routes. SC2 covers distance calculation accuracy against known reference values. SC3 requires nearest-neighbor to always produce a valid tour. SC4 requires 2-opt to never produce a result worse than the nearest-neighbor tour it started from, which is provable by construction and directly demonstrable. SC5 sets an efficiency target at roughly 100 stops, with the exact number confirmed once real benchmarking happens at Hour 29. SC6 requires all invalid input to be rejected without corrupting existing data. SC7 covers the naive-versus-optimized comparison and its visualization.

**Deliverable:** SC1–SC7, locked, full text in planning pack §3.

### Hour 5: Problem decomposition

Break the system into components and map each one to the success criteria it serves: Data Management (SC1), Validation (SC1, SC6), Route Engine (SC2–SC4, SC7), API (SC1, SC5), User Interface (SC7), and Testing (all seven).

**Deliverable:** decomposition tree and SC mapping table, planning pack §4.

### Hour 6: Technology decisions

Choose and justify the stack before building anything. SQLite and SQLAlchemy for relational integrity without server setup. FastAPI for typed validation and automatic docs. HTML, Tailwind, and JavaScript with Leaflet.js for a free, interactive map that needs no API key. The Haversine formula instead of a real road-routing API, avoiding an external dependency while staying a standard, accepted simplification at this scale. pytest for testing.

**Deliverable:** technology decisions table with alternatives considered, planning pack §5.

### Hour 7: System architecture and database design

Design the layering and the schema before writing a single model class. The chain runs from the browser (with the Leaflet map) through FastAPI, a service layer, the route engine, SQLAlchemy, and down to SQLite, kept strictly layered so the engine is testable without the web layer ever running. Three tables: Stop, Route, and RouteStop. `input_order` and `optimized_order` live on the same RouteStop row rather than two separate join tables, so one table produces both the naive and optimized routes without duplicating data. The depot is defined as the stop with `input_order = 0`, avoiding a separate Depot entity. `PRAGMA foreign_keys = ON` is set on every connection for integrity.

**Deliverable:** architecture and ER diagrams, planning pack §6–7.

### Hour 8: Algorithm design

Fully pseudocode every algorithm, with complexity analysis, before implementation begins. Haversine distance runs in O(1) per pair. Total route distance is O(n) for a closed tour that returns to the depot. Nearest-neighbor construction is O(n²). The naive 2-opt implementation runs in O(n³) per sweep, since each of the O(n²) candidate swaps costs O(n) to evaluate by recomputing the whole route; the delta-based swap optimization planned for Hour 30 removes that recompute and drops it to O(n²) per sweep. Everything is checked against a hand-built six-stop worked example: nearest-neighbor comes out 8.8% worse than true optimal on that instance, and 2-opt started from that same suboptimal tour converges to the actual brute-force optimum.

**Deliverable:** full pseudocode and the verified worked example, planning pack §8 and §13.

### Hour 9: UI design

Wireframe the four screens before writing any frontend code. Stop entry: click the map to drop a pin and name it. Route builder: select stops into a named route. Route view, the centerpiece: a naive-versus-optimized toggle over the map, with a stats panel showing both distances and the percentage improvement. Route list: saved routes with quick stats.

**Deliverable:** wireframes, planning pack §9, already using the real worked-example numbers rather than placeholders.

---

## Phase 2: Core Engine (Hours 10–18)

The engine works and is fully tested before FastAPI, SQLAlchemy, or the browser are involved in any of the logic. Everything here is plain Python operating on lists of coordinates.

### Hour 10: Database setup

Create the venv, install `fastapi`, `uvicorn`, `sqlalchemy`, `pytest`. Build `app/database.py`: engine, `SessionLocal`, declarative `Base`, and a `sqlalchemy.event.listens_for(engine, "connect")` handler running `PRAGMA foreign_keys = ON` on every connection, since SQLite doesn't enforce foreign keys otherwise. Build a minimal `app/main.py` with a `GET /health` endpoint that opens and closes a DB session, confirming the full chain connects.

**Deliverable:** `uvicorn app.main:app` boots, `/health` returns 200, the `.db` file exists.

### Hour 11: Database models

Build `app/models.py` with `Stop`, `Route`, and `RouteStop`, matching §7 exactly. Add a unique constraint on `(route_id, stop_id)` so a stop can't be added to the same route twice, and one on `(route_id, input_order)` so two stops can't share a position. Write `tests/test_models.py` immediately: link a stop and a route through `RouteStop`, and confirm inserting a `RouteStop` with a nonexistent `stop_id` raises an `IntegrityError`, which is the actual proof the Hour 10 PRAGMA setting works.

**Deliverable:** tables created via `Base.metadata.create_all`, relationship and FK-rejection tests passing.

### Hour 12: Synthetic data

Build `tests/conftest.py`: a random-stop generator parameterized by count and bounding box, the exact six coordinates from the verified worked example hardcoded, and one or two hand-built shapes (a square, a triangle) with an obvious-by-inspection optimal tour.

**Deliverable:** a fixtures module every later test hour imports from.

### Hour 13: Distance calculation

Build `app/engine/distance.py` with `haversine_distance(a, b)` and `total_distance(ordered_stops)`, matching §8.1–8.2. Sanity-check against one or two independently known real-world city-pair distances before touching the worked example, to validate the raw formula separately from the algorithms that depend on it.

**Deliverable:** `tests/test_distance.py` passing against both reference distances and the worked example's pairwise table.

### Hour 14: Nearest-neighbor construction

Build `app/engine/nearest_neighbor.py` with `nearest_neighbor(stops, depot_index=0)`. Test against the worked example (should match the 13.766 km tour). Also test the trivial cases now: a depot with zero or one other stop, and duplicate coordinates.

**Deliverable:** `tests/test_nearest_neighbor.py`, matched against the worked example's exact numbers.

### Hour 15: 2-opt improvement, naive on purpose

Build `app/engine/two_opt.py` using the naive version from §8.4 exactly as written, full recompute per candidate. Do not optimize yet. Test against the worked example (should produce the 12.657 km tour), an already-optimal small route (should come back unchanged), and a 2-stop route (should come back unchanged since no valid swap exists once the depot is excluded).

**Deliverable:** `tests/test_two_opt.py`, matched against the worked example.

### Hour 16: Route comparison

Build `app/engine/compare.py` per §8.5. Test using the worked example: naive is the NN tour, optimized is the 2-opt tour, improvement should come out to roughly 8.1%.

**Deliverable:** `tests/test_compare.py`.

### Hour 17: Edge-case hardening

Go through every edge case named in §8.5 and §10 as a deliberate checklist: 0 stops, 1 stop, duplicate coordinates, already-optimal input. Decide how the engine signals invalid input (a custom exception like `InvalidRouteError` is cleaner than returning `None`), since this determines how Hour 20's API layer converts failures into HTTP errors.

**Deliverable:** an edge case to expected behavior table.

### Hour 18: Engine test suite, standalone

Run the full `app/engine/` test suite with zero dependency on FastAPI or SQLAlchemy. This is the milestone where the actual computer science already works before a single web request has been handled.

**Deliverable:** a fully green test suite, worth keeping as Criterion D evidence.

---

## Phase 3: Backend & Frontend (Hours 19–26)

### Hour 19: FastAPI foundation

Structure `app/main.py`, `app/routers/`, `app/schemas/`, `app/services/`. Start with `GET /stops` and `GET /routes` to prove FastAPI, the DB session dependency, SQLAlchemy, and SQLite all work together before adding anything more complex.

**Deliverable:** FastAPI serving real DB-backed data, auto-docs visible at `/docs`.

### Hour 20: Stop/route CRUD

Full CRUD for stops and routes (`POST`/`GET`/`PUT`/`DELETE` on `/stops` and `/routes`), plus `POST /routes/{route_id}/stops` and `DELETE /routes/{route_id}/stops/{stop_id}`. Pydantic schemas for creation and reading. Coordinate range validation (`latitude` between -90 and 90, `longitude` between -180 and 180) lives as a Pydantic field validator, a clean, declarative home for SC6's range rule.

**Deliverable:** full CRUD, tested against valid and invalid input (bad ID, out-of-range coordinate, duplicate stop in one route).

### Hour 21: Optimize + compare endpoint

The centerpiece: `POST /routes/{route_id}/optimize`, which runs nearest-neighbor then 2-opt on the route's stops, writes `optimized_order` back, and returns naive and optimized order, both distances, and the improvement percentage. Test by seeding the worked example through the real API and checking the response against §13, the single test proving the entire stack (not just the engine) is correct.

**Deliverable:** one endpoint exercising everything built so far, end to end.

### Hour 22: Frontend base + Leaflet

Static skeleton: `index.html`, Tailwind via CDN, `app.js`, Leaflet loaded via CDN over OpenStreetMap tiles. Get a pannable map rendering and confirm click events report a `(lat, lng)` pair.

**Deliverable:** a blank page with a working map.

### Hour 23: Stop entry + route builder

Wire the click-to-drop-a-pin flow to `POST /stops`. Build the route builder from §9: pick stops, `POST /routes`, then `POST /routes/{id}/stops` for each.

**Deliverable:** stops and routes creatable entirely through the UI.

### Hour 24: Route view

The centerpiece screen: call the optimize endpoint, render both polylines (dashed naive, solid optimized), show the stats panel.

**Deliverable:** the "watch the line get shorter" screen, working against real backend data.

### Hour 25: Frontend validation

Disable "Add Stop" until a pin is dropped, and turn a failed API call's 422 response into a readable message. A second layer of the SC6 reliability story, not a replacement for Hour 20's backend validation.

**Deliverable:** a data-entry flow a normal user can't easily break.

### Hour 26: End-to-end integration

Walk every user flow in the actual browser: create stops, build a route, optimize it, view naive vs. optimized, reopen the route, confirm `optimized_order` persisted. Fix whatever breaks at the seams. Stop adding features after this hour.

**Deliverable:** the complete product, working end to end.

---

## Phase 4: Testing & Optimization (Hours 27–30)

### Hour 27: Reliability testing

Deliberately try to break it: 0-stop route, 1-stop route, duplicate stop added to a route, `latitude = 200`, non-numeric input, deleting a referenced stop, optimizing a route with no stops.

**Deliverable:** an Input, Expected, Actual, Pass/Fail table, every failure fixed before moving on.

### Hour 28: Correctness testing

Re-run the worked example through the real API rather than calling engine functions directly, catching bugs Hour 18's engine-only tests couldn't.

**Deliverable:** a correctness matrix, reusable directly in Criterion D and the final SC matrix.

### Hour 29: Efficiency benchmarking

Generate stop sets at 10, 50, 100, and 500. Time the optimize call at each size, both the raw engine call and the full HTTP round trip separately, to see where any slowness actually comes from.

**Deliverable:** a real benchmark table from your own machine, setting SC5's actual target.

### Hour 30: Optimization

Implement both techniques from §8.4: the precomputed n by n distance matrix, and delta-based swap evaluation (computing only the four edges a candidate swap touches, instead of the whole route). This is the hour with the biggest complexity story: it's a genuine order-of-growth improvement, O(n³) to O(n²) per sweep, not just a constant-factor tweak. Re-run Hour 29's exact benchmark for a real before/after table, and re-run the full worked-example suite to confirm optimizing didn't quietly break correctness.

**Deliverable:** a before/after benchmark table, and confirmation nothing broke.

---

## Phase 5: Finalization (Hours 31–35)

### Hour 31: Final functionality pass

Run through the SC-mapped scenarios fresh: create stops, build a 5+ stop route, optimize it, view naive vs. optimized, submit an invalid stop, run a 100+ stop route. Fix whatever surfaces. Freeze scope.

**Deliverable:** a feature-complete, frozen product.

### Hour 32: Full SC1–SC7 test matrix

Pull together everything from Hours 18, 27, 28, and 29/30 into one final matrix, replacing every placeholder number from §3 and §10 with real ones.

**Deliverable:** the master evidence document Criterion D and E both draw from.

### Hour 33: Criterion D evidence

Select and annotate the strongest excerpts, in priority order: the 2-opt delta optimization with its before/after benchmark, nearest-neighbor construction, the depot-exclusion boundary logic, the FK/PRAGMA integrity setup, and one validation example. WHAT, WHY, HOW, ALTERNATIVE, RESULT for each. Comments get added to excerpts at this stage, even though the working repo itself stays comment-free.

**Deliverable:** a curated Criterion D draft.

### Hour 34: Video and evidence organization

Sequence: open the app, add stops on the map, build a route, show the naive order, run optimize, show the optimized order and improvement percentage, submit an invalid stop and show it rejected, run a 100+ stop route to show it completing quickly, show the Hour 30 before/after benchmark.

**Deliverable:** recorded demonstration, organized evidence folder.

### Hour 35: Evaluation and consistency audit

Build the SC-by-SC evidence table (met, partially met, or not met, and why). Write Criterion E: genuine strengths, genuine weaknesses, and one or two specific, bounded future improvements (Or-opt moves or multiple nearest-neighbor restarts to escape local optima, or multi-vehicle routing from the out-of-scope list). Finish with the full problem-to-evaluation consistency check: does the final product actually answer the problem defined in Hour 1?

**Deliverable:** final evaluation, and a complete, internally consistent IA.
