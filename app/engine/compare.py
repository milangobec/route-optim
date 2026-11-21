from typing import NamedTuple

from app.engine.distance import total_distance
from app.engine.types import Coordinate


class ComparisonResult(NamedTuple):
    naive_distance_km: float
    optimized_distance_km: float
    improvement_percent: float


def compare_routes(
    naive_order: list[Coordinate], optimized_order: list[Coordinate]
) -> ComparisonResult:
    naive_distance = total_distance(naive_order)
    optimized_distance = total_distance(optimized_order)

    if naive_distance == 0:
        improvement_percent = 0.0
    else:
        improvement_percent = (naive_distance - optimized_distance) / naive_distance * 100

    return ComparisonResult(naive_distance, optimized_distance, improvement_percent)
