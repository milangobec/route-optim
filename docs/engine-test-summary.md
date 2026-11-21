# Engine Test Summary (Hour 18)

Evidence that the route engine works on its own, before any web request is handled. A passing suite only counts if it can also fail, so this document includes a mutation check: deliberately broken versions of the engine, and which test catches each.

## Results

| Measure | Result |
|---|---|
| Tests in the full suite | 49 |
| Engine tests that run with sqlalchemy and fastapi blocked from importing | 38 |
| Line and branch coverage of app/engine | 100% (77 statements, 18 branches) |
| Deliberate bugs caught | 6 of 6 |

## Commands to reproduce

```
uv run pytest
uv run python -m scripts.run_engine_tests_isolated
uv run pytest --cov=app/engine --cov-branch --cov-report=term-missing
uv run python -m scripts.mutation_check
```

The isolated run replaces sqlalchemy and fastapi with unimportable placeholders before pytest starts, so any engine test that secretly depends on the web or database stack would error. tests/test_engine_isolation.py additionally imports every module in app/engine in a fresh process and checks that none of sqlalchemy, fastapi, pydantic, or starlette were loaded.

## Edge cases

| Edge case | nearest_neighbor | two_opt | compare_routes |
|---|---|---|---|
| Empty list | raises InvalidRouteError (test_edge_cases) | precondition: a route from nearest_neighbor, not validated separately | precondition: same, not validated separately |
| 1 stop (depot only) | returns [depot] (test_nearest_neighbor) | returns it unchanged (test_edge_cases) | both distances 0, improvement 0% (test_compare) |
| 2 stops | returns both in order (test_nearest_neighbor) | no candidate pair, unchanged (test_two_opt) | improvement 0%, distance above 0 (test_edge_cases) |
| Duplicate coordinates | completes without error (test_nearest_neighbor) | full pipeline completes (test_edge_cases) | improvement 0% (test_edge_cases) |
| Already-optimal input (square) | finds the perimeter (test_nearest_neighbor) | unchanged (test_two_opt) | improvement 0% (test_compare) |
| Two stops tied for nearest | tie-break picks the one farther from the remaining centroid (test_nearest_neighbor) | not applicable | not applicable |
| Floating-point noise between equal tours | not applicable | triangle fed directly stays unchanged (test_invariants) | not applicable |
| Input list reused by the caller | not mutated (test_invariants) | not mutated (test_invariants) | not applicable |

## Success criteria to tests

| SC | Covered by |
|---|---|
| SC2 | test_distance: BNA to LAX reference distance, all 15 pairwise distances from the worked example, symmetry, zero distance, both tour totals |
| SC3 | test_invariants: 100 of 100 random sets (1 to 40 stops besides the depot) give a valid tour, depot first and every stop exactly once; worked example and square in test_nearest_neighbor |
| SC4 | test_two_opt: never worse than its input across 100 random sets (2 to 30 stops); test_invariants: output is still a valid tour for 100 of 100 random sets; worked example reaches 12.657 km |
| SC7 (engine side) | test_compare: worked example gives 13.766 km, 12.657 km, 8.06% improvement; no-improvement and zero-distance cases |

SC1, SC5, and SC6 involve the database, API, and benchmarks, and are evidenced in later hours.

## Mutation check

Each row is one line of the engine changed on purpose, run against a temporary copy of the project (scripts/mutation_check.py), so the real files are never touched.

| Deliberate bug | Before Hour 18 | After Hour 18 | Caught by |
|---|---|---|---|
| 2-opt swap range starts at index 0, so the depot can move | survived | caught | test_two_opt_keeps_a_valid_tour_for_100_random_sets |
| 2-opt improvement tolerance removed | survived | caught | test_two_opt_leaves_triangle_unchanged_when_fed_directly |
| Tie-break picks the stop nearer the centroid | caught | caught | test_tie_breaks_toward_stop_farther_from_remaining_centroid |
| total_distance drops the return-to-depot leg | caught | caught | 7 tests across distance, nearest-neighbor, 2-opt, compare, and edge cases |
| Wrong Earth radius (6378 km) | caught | caught | 7 tests, including the BNA to LAX reference |
| compare_routes divide-by-zero guard removed | caught | caught | test_single_stop_route_reports_zero_percent_without_error |

The two bugs that survived before Hour 18 were both invisible to distance-based tests. Moving the depot does not change a closed tour's length, and the Hour 15 tolerance test sent the triangle through nearest_neighbor first, which happens to put the stops in the order where the noisy swap is never the smaller candidate. Both are now caught by tests that check the output's structure and feed the triangle in directly.
