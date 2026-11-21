# Success Criteria (Hour 4)

Locked once written up, everything downstream (plan, testing, evaluation) refers back to these. Placeholder numeric targets (marked TBD) get confirmed empirically at the Hour 29 benchmarking step, that's normal implementation validation, not an open research question.

**SC1, Data management.** Create, retrieve, modify, and delete valid stops and routes while maintaining valid relationships between them. 99% or more of valid CRUD operations succeed; invalid foreign-key relationships are rejected without creating orphaned records.

**SC2, Distance calculation.** Correctly calculate the distance between two stops and the total distance of a route, matching independently calculated reference values within 0.01 km.

**SC3, Route construction.** The nearest-neighbor algorithm produces a valid tour, every stop visited exactly once, starting and ending at the depot, for at least 95 out of 100 randomly generated stop sets of varying size.

**SC4, Route optimization.** For every tested route, the 2-opt-optimized total distance is never greater than the nearest-neighbor route it started from. This is provable by construction (2-opt only ever accepts a swap that shortens the route), so this SC is really a test that the implementation doesn't violate its own guarantee. Clean, crisp, and directly demonstrable in the video.

**SC5, Efficiency.** Construct and optimize a route of at least 100 stops within [TBD, target roughly 3 seconds] on the development machine, for at least 95 out of 100 repeated runs.

**SC6, Reliability.** Reject 100% of deliberately invalid inputs (out-of-range coordinates, non-numeric fields, duplicate stop in one route, nonexistent foreign keys) without corrupting existing records.

**SC7, Comparison and visualization.** Display the naive-order route and the optimized route on a map with their respective total distances and percentage improvement, matching the analytical engine's own output.
