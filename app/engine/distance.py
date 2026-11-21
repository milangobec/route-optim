import math

from app.engine.types import Coordinate

EARTH_RADIUS_KM = 6371.0


def haversine_distance(a: Coordinate, b: Coordinate) -> float:
    lat1 = math.radians(a.latitude)
    lat2 = math.radians(b.latitude)
    delta_lat = math.radians(b.latitude - a.latitude)
    delta_lon = math.radians(b.longitude - a.longitude)

    h = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))
    return EARTH_RADIUS_KM * c


def total_distance(ordered_stops: list[Coordinate]) -> float:
    total = 0.0
    for i in range(len(ordered_stops) - 1):
        total += haversine_distance(ordered_stops[i], ordered_stops[i + 1])
    total += haversine_distance(ordered_stops[-1], ordered_stops[0])
    return total
