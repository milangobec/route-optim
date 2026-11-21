from app.engine.distance import haversine_distance
from app.engine.exceptions import InvalidRouteError
from app.engine.types import Coordinate

TIE_TOLERANCE_KM = 1e-9


def nearest_neighbor(stops: list[Coordinate], depot_index: int = 0) -> list[Coordinate]:
    if not stops:
        raise InvalidRouteError("nearest_neighbor requires at least one stop (the depot)")

    depot = stops[depot_index]
    unvisited = [s for i, s in enumerate(stops) if i != depot_index]
    route = [depot]
    current = depot

    while unvisited:
        min_distance = min(haversine_distance(current, s) for s in unvisited)
        tied = [
            s
            for s in unvisited
            if abs(haversine_distance(current, s) - min_distance) < TIE_TOLERANCE_KM
        ]

        if len(tied) == 1:
            next_stop = tied[0]
        else:
            centroid_lat = sum(s.latitude for s in unvisited) / len(unvisited)
            centroid_lon = sum(s.longitude for s in unvisited) / len(unvisited)
            centroid = Coordinate("centroid", centroid_lat, centroid_lon)
            next_stop = max(tied, key=lambda s: haversine_distance(s, centroid))

        route.append(next_stop)
        unvisited.remove(next_stop)
        current = next_stop

    return route
