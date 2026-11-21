import pytest

from app.engine.compare import compare_routes
from app.engine.distance import total_distance
from app.engine.nearest_neighbor import nearest_neighbor
from app.engine.two_opt import two_opt
from app.engine.types import Coordinate


def test_matches_worked_example_improvement(worked_example_stops):
    naive_order = nearest_neighbor(worked_example_stops, depot_index=0)
    optimized_order = two_opt(naive_order)

    result = compare_routes(naive_order, optimized_order)

    assert result.naive_distance_km == pytest.approx(13.766, abs=0.01)
    assert result.optimized_distance_km == pytest.approx(12.657, abs=0.01)
    assert result.improvement_percent == pytest.approx(8.06, abs=0.1)


def test_no_improvement_reports_zero_percent(square_stops):
    naive_order = nearest_neighbor(square_stops, depot_index=0)
    optimized_order = two_opt(naive_order)

    result = compare_routes(naive_order, optimized_order)

    assert result.improvement_percent == pytest.approx(0.0, abs=1e-6)


def test_single_stop_route_reports_zero_percent_without_error():
    depot = Coordinate("Depot", 41.878100, -87.629800)

    result = compare_routes([depot], [depot])

    assert result.naive_distance_km == 0.0
    assert result.optimized_distance_km == 0.0
    assert result.improvement_percent == 0.0


def test_distances_match_total_distance_independently(worked_example_stops):
    naive_order = nearest_neighbor(worked_example_stops, depot_index=0)
    optimized_order = two_opt(naive_order)

    result = compare_routes(naive_order, optimized_order)

    assert result.naive_distance_km == total_distance(naive_order)
    assert result.optimized_distance_km == total_distance(optimized_order)
