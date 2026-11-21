import pytest

from app.engine.distance import haversine_distance, total_distance
from app.engine.types import Coordinate

BNA = Coordinate("BNA", 36.12, -86.67)
LAX = Coordinate("LAX", 33.94, -118.40)

PAIRWISE_KM = {
    ("Depot", "A"): 3.517,
    ("Depot", "B"): 1.700,
    ("Depot", "C"): 2.862,
    ("Depot", "D"): 2.381,
    ("Depot", "E"): 0.727,
    ("A", "B"): 4.356,
    ("A", "C"): 0.751,
    ("A", "D"): 5.654,
    ("A", "E"): 3.710,
    ("B", "C"): 3.608,
    ("B", "D"): 1.481,
    ("B", "E"): 2.367,
    ("C", "D"): 4.924,
    ("C", "E"): 3.145,
    ("D", "E"): 2.758,
}


def test_haversine_matches_bna_to_lax_reference():
    distance = haversine_distance(BNA, LAX)
    assert distance == pytest.approx(2886.44, abs=0.01)


def test_haversine_distance_to_self_is_zero():
    point = Coordinate("Point", 41.8781, -87.6298)
    assert haversine_distance(point, point) == pytest.approx(0.0, abs=1e-9)


def test_haversine_is_symmetric():
    assert haversine_distance(BNA, LAX) == pytest.approx(
        haversine_distance(LAX, BNA), abs=1e-9
    )


def test_haversine_matches_worked_example_pairwise_table(worked_example_stops):
    by_name = {stop.name: stop for stop in worked_example_stops}
    for (name_a, name_b), expected_km in PAIRWISE_KM.items():
        actual = haversine_distance(by_name[name_a], by_name[name_b])
        assert actual == pytest.approx(expected_km, abs=0.01)


def test_total_distance_matches_nearest_neighbor_tour(worked_example_stops):
    by_name = {stop.name: stop for stop in worked_example_stops}
    nn_order = [by_name[name] for name in ["Depot", "E", "B", "D", "C", "A"]]
    assert total_distance(nn_order) == pytest.approx(13.766, abs=0.01)


def test_total_distance_matches_two_opt_tour(worked_example_stops):
    by_name = {stop.name: stop for stop in worked_example_stops}
    two_opt_order = [by_name[name] for name in ["Depot", "D", "B", "C", "A", "E"]]
    assert total_distance(two_opt_order) == pytest.approx(12.657, abs=0.01)
