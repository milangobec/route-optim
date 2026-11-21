# 2-opt Improvement (Hour 8.4, extended Hour 15)

```
FUNCTION twoOpt(route)
    improved = true
    best = route
    WHILE improved
        improved = false
        FOR i = 1 TO length(best) - 2
            FOR j = i + 1 TO length(best) - 1
                candidate = reverse the segment of best between i and j
                IF totalDistance(candidate) < totalDistance(best)
                    best = candidate
                    improved = true
    RETURN best
```

O(n squared) candidate pairs are checked per full sweep. As written above, each candidate is evaluated by recomputing the entire route's distance, which costs O(n), so this naive version runs in O(n cubed) per sweep, deliberately left unoptimized until Hour 30. The number of sweeps needed until no improving swap remains isn't tightly bounded in the worst case, but for problem sizes here (tens to a few hundred stops) it converges within a small number of passes in practice. Supports SC4.

## Design decision: first-improvement, not best-improvement

The pseudocode above accepts and applies the first improving swap it finds within a pass, then keeps scanning from the updated tour rather than evaluating every candidate pair first and applying only the single best one. This is the first-improvement variant of 2-opt, not best-improvement. First-improvement was chosen because it's simpler to implement correctly and reason about, converges in practice for problem sizes at this scale, and is the variant most commonly described in introductory treatments of the algorithm. Best-improvement would cost an extra full pass per swap to find the single best candidate, for no accuracy benefit at this scale.

## Depot exclusion

The outer loop starts at index 1, never 0, so the reversed segment can never include the depot. If it started at 0, the depot could move out of position 0. A closed tour's length does not depend on where it starts, so every distance-based test would still pass. Only a test that asserts the depot stays first and every stop appears exactly once catches this, and that test exists (tests/test_invariants.py).

## Correctness fix found during testing: floating-point tolerance on the improvement check

A strict `<` comparison between two floating-point total distances can spuriously evaluate true when two orderings are mathematically identical but differ by a rounding error far smaller than any real improvement. This happened on the Hour 12 triangle fixture, where reversing the only two non-depot stops produces the same tour walked in the opposite direction, and the two computed totals differed by 4.4e-16 km, far below any meaningful distance, but enough to make Python's `<` return true. Fixed with a small improvement tolerance (1e-9 km): a candidate is only accepted if it beats the current best by more than that margin. Without this, the algorithm could reorder an already-optimal tour based on nothing but rounding noise.

The regression test feeds the triangle fixture directly into two_opt. Routing it through nearest_neighbor first happens to order it so the noisy swap is never the smaller candidate, which hides the bug.

## Known optimization targets for Hour 30, in order of impact

1. Avoid recomputing the whole route. Compute only the change in length a candidate swap would cause, the two edges being removed minus the two edges being added. If that change is negative, the swap improves the tour, with no need to re-sum the whole route. Turns each candidate check from O(n) into O(1).
2. Precompute a distance matrix. An n by n table of every pairwise Haversine distance, built once (O(n squared) up front), turns every subsequent lookup into an O(1) array read instead of a fresh trig calculation.

Both are standard, documented optimizations for this exact algorithm (see research-log.md), not something invented from scratch.

## Known limitation for Criterion E

2-opt can get stuck in a local optimum. A specific, bounded future improvement: add Or-opt moves (relocate a single stop rather than only reversing segments) or restart from multiple nearest-neighbor seeds and keep the best result.
