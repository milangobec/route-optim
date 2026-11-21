# Research Log: Route Optimizer (Hour 2)

Format: Source / What I learned / How it affects the system, same convention as before.

---

**Source:** "Nearest neighbour algorithm", Wikipedia
**What I learned:** The nearest-neighbor heuristic starts at an arbitrary vertex and repeatedly moves to the closest unvisited vertex until every vertex has been visited. It's simple, fast (worst-case Theta(n squared)), and not guaranteed optimal. For some pathological instances its result can be arbitrarily far worse than the true optimum.
**How it affects the system:** Confirms nearest-neighbor is a legitimate, well-precedented choice for the initial construction step (R7), but also confirms why a separate improvement step is necessary rather than treating NN's output as final. It directly justifies pairing it with 2-opt rather than stopping at construction.

---

**Source:** "A Heuristic Algorithm Based on Tour Rebuilding Operator for the Traveling Salesman Problem" (arXiv preprint)
**What I learned:** Nearest-neighbor's point-by-point tour construction is one of the earliest TSP approaches, valued for being easy to implement and efficient, but too greedy to reliably reach a global optimum. More advanced local-search methods (2-opt, 3-opt, Lin-Kernighan) build directly on top of this same construction step rather than replacing it.
**How it affects the system:** Validates the two-stage design (cheap greedy construction, then local-search improvement) as a standard, recognized pattern in the literature, not something invented ad hoc. Good citable justification for the architecture in Criterion D.

---

**Source:** "2-opt", Wikipedia
**What I learned:** 2-opt was formally proposed by Croes in 1958, building on a swap idea suggested earlier by Flood in 1956. It works by taking a route that crosses over itself and reordering the crossing segment so the crossing disappears, repeating until no further improving swap exists. The node(s) at the fixed start/end of the route must be excluded from the swappable range, since swapping them would produce an invalid tour that no longer starts and ends at the depot.
**How it affects the system:** Confirms the depot must be explicitly excluded from the swap index range in the implementation, a concrete detail to test directly (a 2-stop-plus-depot edge case, and a check that the depot position never moves). Also gives a decades-old, well-established provenance for the technique, which strengthens the "why this algorithm" argument in Criterion D.

---

**Source:** "2-opt", Wikipedia (implementation notes)
**What I learned:** Rather than recomputing the full route length for every candidate swap, it's possible to compute just the change in length a swap would cause, the two edges removed minus the two edges added. If that change is negative, the swap is an improvement, without ever re-summing the whole route.
**How it affects the system:** This becomes the Hour 30-equivalent optimization: replacing a full route recalculation per candidate swap (O(n)) with a constant-time delta check, on top of a precomputed distance matrix. A second, independently documented optimization opportunity, see the updated two-opt.md.

---

**Source:** "Haversine formula", Wikipedia
**What I learned:** The haversine formula computes the great-circle (shortest surface-path) distance between two points on a sphere from their latitudes and longitudes. It's a long-standing navigation formula, traceable to the early 1800s, not a novel or unproven method.
**How it affects the system:** Confirms Haversine as a standard, well-precedented choice for distance calculation (R5) rather than something needing to be independently validated from scratch, though the implementation still gets sanity-checked against a couple of independently known reference distances (SC2).

---

**Source:** Codemia, "Calculate distance between two latitude-longitude points (Haversine formula)"
**What I learned:** A typical implementation converts degrees to radians before applying the trigonometric functions. The formula gives straight-line surface distance only, not actual road-network travel distance, a simplification that is explicitly and routinely accepted for mapping, navigation, and geofencing tasks generally, not just for student projects.
**How it affects the system:** Independent confirmation that "Haversine as an accepted simplification vs. true road distance" is a mainstream, defensible framing for the technology-decisions table, not a corner cut to save time.

---

## Summary of decisions this research supports

| Decision | Supported by |
|---|---|
| Use nearest-neighbor for initial construction | Standard, well-documented TSP construction heuristic |
| Pair it with 2-opt rather than stopping at NN | NN alone is not optimal and can be arbitrarily bad in the worst case |
| Exclude the depot from swap range in 2-opt | Swapping the fixed endpoint produces an invalid tour |
| Use delta-based swap evaluation + precomputed distance matrix at Hour 30 | Both are standard, documented optimizations for this exact algorithm |
| Use Haversine rather than a routing API | Long-established, widely-accepted simplification for this class of problem |

No open questions here that need empirical resolution. Every choice above is either a cited, established technique or a stated design simplification with a clear justification. That's the deliberate difference from the old project's research phase.
