from app.engine.distance import total_distance
from app.engine.types import Coordinate

IMPROVEMENT_TOLERANCE_KM = 1e-9


def two_opt(route: list[Coordinate]) -> list[Coordinate]:
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 1):
            for j in range(i + 1, len(best)):
                candidate = best[:i] + best[i : j + 1][::-1] + best[j + 1 :]
                if total_distance(candidate) < total_distance(best) - IMPROVEMENT_TOLERANCE_KM:
                    best = candidate
                    improved = True
    return best
