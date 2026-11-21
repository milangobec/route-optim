# Worked Example, Correctness and Testing Anchor (Hour 8, supports Hour 12 and Hour 18)

A small, fully hand-verifiable case, computed and cross-checked against a brute-force search over every possible ordering (feasible only because n is tiny here). This is the anchor test case for SC2, SC3, and SC4 once the engine exists, and it can be dropped in directly as pytest fixtures rather than invented from scratch later.

## Stops (Depot + 5, small local area, fictional coordinates near no real address)

| Label | Latitude | Longitude |
|---|---|---|
| Depot | 41.878100 | -87.629800 |
| A | 41.852291 | -87.654357 |
| B | 41.873571 | -87.610189 |
| C | 41.855528 | -87.646406 |
| D | 41.885746 | -87.602937 |
| E | 41.882726 | -87.635999 |

## Pairwise Haversine distances (km)

| | A | B | C | D | E |
|---|---|---|---|---|---|
| Depot | 3.517 | 1.700 | 2.862 | 2.381 | 0.727 |
| A | - | 4.356 | 0.751 | 5.654 | 3.710 |
| B | - | - | 3.608 | 1.481 | 2.367 |
| C | - | - | - | 4.924 | 3.145 |
| D | - | - | - | - | 2.758 |

## Results

**Nearest-neighbor tour (starting at Depot):** Depot to E to B to D to C to A back to Depot = 13.766 km

**2-opt-improved tour:** Depot to D to B to C to A to E back to Depot = 12.657 km

**True optimal tour (brute-force over all 120 possible orderings):** Depot to E to A to C to B to D back to Depot = 12.657 km

The 2-opt result and the brute-force optimum are the same cycle, just traversed in opposite directions, expected, since a closed tour has identical length either way round.

## What this demonstrates

- Nearest-neighbor's greedy choice leaves it 8.8% longer than true optimal on this input, a concrete, real demonstration of the textbook point that NN is not optimal, not just an assertion.
- 2-opt, started from that suboptimal NN tour, converges to the actual global optimum on this input. It won't always reach the true global optimum on larger instances, no local search can guarantee that, but this confirms the implementation does what it's supposed to on a case small enough to fully verify by brute force.
- Gives exact numbers to assert directly in tests, for example checking that the NN tour distance is within 0.01 of 13.766, and the same for the 2-opt and optimal cases.

This example was found by generating random small stop sets and keeping the first one that showed a genuine NN versus optimal gap, a deliberately chosen test case, not a cherry-picked one that hides a bug, the same logic behind the previous project's hand-built improving/stable/declining synthetic sets.
