# Testing Strategy Preview (supports Hour 9, filled in fully at Hours 18, 27, 28, 32)

| SC | Typical case | Boundary case | Abnormal case |
|---|---|---|---|
| SC2 | Known city-pair distance, hand-calculated | Identical coordinates, 0 distance | Latitude out of range (e.g. 200) |
| SC3 | 10 random stops, valid tour produced | 1 stop, 2 stops | Duplicate stop in input |
| SC4 | 20+ random stops, optimized <= NN | Already-optimal small tour (e.g. a square) | 2-stop route (no possible improvement) |
| SC5 | 100 stops within target time | 10 stops (should be near-instant) | 500+ stops (identify the ceiling) |
| SC6 | - | - | Bad coordinates, missing FK, non-numeric input |
| SC7 | Comparison matches engine output | Naive equals optimized (no improvement found) | - |

Full test tables (Input, Expected, Actual, Pass/Fail) get built out at the Hour 18/28-equivalent stages, same format as the previous project.
