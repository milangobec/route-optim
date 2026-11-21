import pytest

from app.engine.compare import compare_routes
from app.engine.exceptions import InvalidRouteError
from app.engine.nearest_neighbor import nearest_neighbor
from app.engine.two_opt import two_opt
from app.engine.types import Coordinate


def test_empty_stops_raises_invalid_route_error():
    with pytest.raises(InvalidRouteError):
        nearest_neighbor([])


def test_duplicate_coordinates_through_full_pipeline():
    depot = Coordinate("Depot", 41.878100, -87.629800)
    stop_a = Coordinate("StopA", 41.885000, -87.620000)
    stop_b = Coordinate("StopB", 41.885000, -87.620000)
    stop_c = Coordinate("StopC", 41.870000, -87.640000)

    naive_order = nearest_neighbor([depot, stop_a, stop_b, stop_c], depot_index=0)
    optimized_order = two_opt(naive_order)
    result = compare_routes(naive_order, optimized_order)

    assert len(naive_order) == 4
    assert len(optimized_order) == 4
    assert result.naive_distance_km == pytest.approx(4.7016, abs=0.001)
    assert result.optimized_distance_km == pytest.approx(4.7016, abs=0.001)
    assert result.improvement_percent == pytest.approx(0.0, abs=1e-6)


def test_two_opt_single_stop_route_returns_unchanged():
    depot = Coordinate("Depot", 41.878100, -87.629800)

    assert two_opt([depot]) == [depot]


def test_two_stop_route_reports_zero_percent_improvement():
    depot = Coordinate("Depot", 41.878100, -87.629800)
    only_stop = Coordinate("OnlyStop", 41.885000, -87.620000)

    route = nearest_neighbor([depot, only_stop], depot_index=0)
    result = compare_routes(route, two_opt(route))

    assert result.improvement_percent == pytest.approx(0.0, abs=1e-6)
    assert result.naive_distance_km > 0
