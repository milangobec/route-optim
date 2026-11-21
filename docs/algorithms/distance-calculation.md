# Distance Calculation (Hour 8.1-8.2)

## Haversine distance

```
FUNCTION haversineDistance(stopA, stopB)
    R = 6371
    lat1 = radians(stopA.latitude)
    lat2 = radians(stopB.latitude)
    dLat = radians(stopB.latitude - stopA.latitude)
    dLon = radians(stopB.longitude - stopA.longitude)
    a = sin(dLat / 2)^2 + cos(lat1) * cos(lat2) * sin(dLon / 2)^2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    RETURN R * c
```

O(1) per pair. Supports SC2.

## Total route distance (closed tour, returns to depot)

```
FUNCTION totalDistance(orderedStops)
    total = 0
    FOR i = 0 TO length(orderedStops) - 2
        total += haversineDistance(orderedStops[i], orderedStops[i + 1])
    total += haversineDistance(orderedStops[last], orderedStops[0])
    RETURN total
```

O(n). Supports SC2.
