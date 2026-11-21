import random

import pytest

from app.engine.distance import haversine_distance, total_distance
from app.engine.nearest_neighbor import nearest_neighbor
from app.engine.types import Coordinate


def test_matches_worked_example_tour(worked_example_stops):
    route = nearest_neighbor(worked_example_stops, depot_index=0)
    assert total_distance(route) == pytest.approx(13.766, abs=0.01)


def test_matches_square_perimeter(square_stops):
    route = nearest_neighbor(square_stops, depot_index=0)
    names = [stop.name for stop in route]
    assert names == ["Depot", "B", "C", "D"]


def test_tie_breaks_toward_stop_farther_from_remaining_centroid():
    depot = Coordinate("Depot", 41.878100, -87.629800)
    stop_x = Coordinate("StopX", 41.878100, -87.619800)
    stop_y = Coordinate("StopY", 41.878100, -87.639800)
    stop_z = Coordinate("StopZ", 41.900000, -87.600000)

    route = nearest_neighbor([depot, stop_x, stop_y, stop_z], depot_index=0)

    assert [stop.name for stop in route] == ["Depot", "StopY", "StopX", "StopZ"]


def test_tie_frequency_on_realistic_random_data():
    random.seed(42)
    total_steps = 0
    exact_ties = 0

    for _ in range(1000):
        stops = [Coordinate("Depot", 41.878100, -87.629800)]
        for i in range(8):
            lat = random.uniform(41.86, 41.90)
            lon = random.uniform(-87.66, -87.60)
            stops.append(Coordinate(f"Stop {i}", lat, lon))

        unvisited = stops[1:]
        current = stops[0]
        while unvisited:
            distances = sorted(haversine_distance(current, s) for s in unvisited)
            total_steps += 1
            if len(distances) > 1 and abs(distances[0] - distances[1]) < 1e-9:
                exact_ties += 1
            next_stop = min(unvisited, key=lambda s: haversine_distance(current, s))
            unvisited.remove(next_stop)
            current = next_stop

    assert total_steps == 8000
    assert exact_ties == 0


def test_single_additional_stop_returns_trivial_route():
    depot = Coordinate("Depot", 41.878100, -87.629800)
    only_stop = Coordinate("OnlyStop", 41.885000, -87.620000)

    route = nearest_neighbor([depot, only_stop], depot_index=0)

    assert [stop.name for stop in route] == ["Depot", "OnlyStop"]


def test_no_additional_stops_returns_just_depot():
    depot = Coordinate("Depot", 41.878100, -87.629800)

    route = nearest_neighbor([depot], depot_index=0)

    assert [stop.name for stop in route] == ["Depot"]


def test_duplicate_coordinates_do_not_error():
    depot = Coordinate("Depot", 41.878100, -87.629800)
    stop_a = Coordinate("StopA", 41.885000, -87.620000)
    stop_b = Coordinate("StopB", 41.885000, -87.620000)

    route = nearest_neighbor([depot, stop_a, stop_b], depot_index=0)

    assert len(route) == 3
    assert {stop.name for stop in route} == {"Depot", "StopA", "StopB"}
