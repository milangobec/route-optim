# Route Comparison (Hour 8.5)

```
FUNCTION compareRoutes(naiveOrder, optimizedOrder)
    naiveDistance = totalDistance(naiveOrder)
    optimizedDistance = totalDistance(optimizedOrder)
    improvementPercent = (naiveDistance - optimizedDistance) / naiveDistance * 100
    RETURN naiveDistance, optimizedDistance, improvementPercent
```

Supports SC7.

## Edge cases to design for now, test later

- 0 or 1 stop: trivial, distance is 0, no optimization needed.
- 2 stops: only one possible round trip, 2-opt should make no change.
- Duplicate coordinates: distance of 0 between them.
- An already-optimal input: 2-opt should terminate immediately with no improvement.
