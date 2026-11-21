# Nearest-Neighbor Construction (Hour 8.3, extended Hour 14)

```
FUNCTION nearestNeighbor(stops, depot)
    unvisited = allStops except depot
    route = [depot]
    current = depot
    WHILE unvisited is not empty
        next = stop in unvisited minimizing haversineDistance(current, stop)
        route.append(next)
        remove next from unvisited
        current = next
    RETURN route
```

O(n squared). Supports SC3.

## Original addition: tie-breaking rule

The standard description above, and most textbook writeups of nearest-neighbor, don't specify what happens when two or more unvisited stops are equally close to the current stop. That gap is filled here with a deliberate rule: when multiple stops are tied for nearest (within a small floating-point tolerance, 1e-9 km, since two geometrically identical distances computed through different trigonometric paths can differ by a tiny rounding error even when they represent a genuine tie), the tied candidate that sits farther from the centroid of the remaining unvisited stops is chosen.

Reasoning: if two stops are equally cheap to reach right now, the one closer to the rest of the unvisited cluster will still be reasonably convenient later, once its neighbors are visited. The one farther from that cluster only gets more expensive to reach the longer it's left, so it gets picked first.

## Measured impact, not just asserted

Across 1,000 randomly generated 9-stop trials (8,000 individual nearest-neighbor construction steps), zero exact ties occurred, even within a tolerance of 1e-6 km. This confirms the rule cannot be expected to activate on realistic or randomly generated data; it exists for a genuine but rare edge case. A dedicated test case (two stops placed as exact mirror images across the current point) was built specifically to exercise it, since natural test data never will.

Verified against the worked example (Depot to E to B to D to C to A, 13.766 km) and the Hour 12 square fixture (perimeter order, Depot to B to C to D): the tie-breaking addition changes nothing when there is no tie, both cases still match exactly.

## Empty input

An empty list of stops raises InvalidRouteError rather than an unhelpful IndexError. This is the single validation point for the engine: two_opt and compare_routes assume they are given a route that nearest_neighbor produced.
