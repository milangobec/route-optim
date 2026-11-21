import random

import pytest

from app.engine.distance import total_distance
from app.engine.nearest_neighbor import nearest_neighbor
from app.engine.two_opt import two_opt
from app.engine.types import Coordinate


def test_matches_worked_example_tour(worked_example_stops):
    nn_route = nearest_neighbor(worked_example_stops, depot_index=0)
    optimized = two_opt(nn_route)
    assert total_distance(optimized) == pytest.approx(12.657, abs=0.01)


def test_already_optimal_square_unchanged(square_stops):
    nn_route = nearest_neighbor(square_stops, depot_index=0)
    optimized = two_opt(nn_route)
    assert optimized == nn_route


def test_minimal_triangle_case_unchanged(triangle_stops):
    nn_route = nearest_neighbor(triangle_stops, depot_index=0)
    optimized = two_opt(nn_route)
    assert optimized == nn_route


def test_two_node_route_has_no_candidate_pairs():
    depot = Coordinate("Depot", 41.878100, -87.629800)
    only_stop = Coordinate("OnlyStop", 41.885000, -87.620000)
    route = [depot, only_stop]

    optimized = two_opt(route)

    assert optimized == route


def test_never_produces_a_worse_tour_than_its_input():
    random.seed(7)
    for trial in range(100):
        count = random.randint(2, 30)
        stops = [Coordinate("Depot", 41.878100, -87.629800)]
        for i in range(count):
            lat = random.uniform(41.86, 41.90)
            lon = random.uniform(-87.66, -87.60)
            stops.append(Coordinate(f"Stop {i}", lat, lon))

        nn_route = nearest_neighbor(stops, depot_index=0)
        optimized = two_opt(nn_route)

        assert total_distance(optimized) <= total_distance(nn_route) + 1e-9
