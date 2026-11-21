import random

from app.engine.nearest_neighbor import nearest_neighbor
from app.engine.two_opt import two_opt
from app.engine.types import Coordinate

DEPOT = Coordinate("Depot", 41.878100, -87.629800)


def make_stops(rng, count):
    stops = [DEPOT]
    for i in range(count):
        stops.append(
            Coordinate(
                f"Stop {i}",
                rng.uniform(41.86, 41.90),
                rng.uniform(-87.66, -87.60),
            )
        )
    return stops


def is_valid_tour(tour, original):
    return (
        tour[0] == original[0]
        and len(tour) == len(original)
        and sorted(tour) == sorted(original)
    )


def test_nearest_neighbor_builds_a_valid_tour_for_100_random_sets():
    rng = random.Random(2024)
    valid = 0
    for _ in range(100):
        stops = make_stops(rng, rng.randint(1, 40))
        if is_valid_tour(nearest_neighbor(stops), stops):
            valid += 1

    assert valid == 100


def test_two_opt_keeps_a_valid_tour_for_100_random_sets():
    rng = random.Random(2025)
    valid = 0
    for _ in range(100):
        stops = make_stops(rng, rng.randint(2, 20))
        if is_valid_tour(two_opt(nearest_neighbor(stops)), stops):
            valid += 1

    assert valid == 100


def test_two_opt_leaves_triangle_unchanged_when_fed_directly(triangle_stops):
    assert two_opt(triangle_stops) == triangle_stops


def test_nearest_neighbor_does_not_mutate_its_input(worked_example_stops):
    before = list(worked_example_stops)

    nearest_neighbor(worked_example_stops)

    assert worked_example_stops == before


def test_two_opt_does_not_mutate_its_input(worked_example_stops):
    route = nearest_neighbor(worked_example_stops)
    before = list(route)

    two_opt(route)

    assert route == before
