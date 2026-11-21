def test_worked_example_stops_structure(worked_example_stops):
    assert len(worked_example_stops) == 6
    names = [stop.name for stop in worked_example_stops]
    assert names == ["Depot", "A", "B", "C", "D", "E"]


def test_square_stops_structure(square_stops):
    assert len(square_stops) == 4
    assert square_stops[0].name == "Depot"


def test_triangle_stops_structure(triangle_stops):
    assert len(triangle_stops) == 3
    assert triangle_stops[0].name == "Depot"


def test_random_stops_factory_produces_requested_count(random_stops_factory):
    stops = random_stops_factory(count=10, seed=42)
    assert len(stops) == 11
    assert stops[0].name == "Depot"


def test_random_stops_factory_is_reproducible_with_seed(random_stops_factory):
    a = random_stops_factory(count=5, seed=123)
    b = random_stops_factory(count=5, seed=123)
    assert a == b


def test_random_stops_stay_within_bounding_box(random_stops_factory):
    stops = random_stops_factory(count=20, seed=1)
    for stop in stops[1:]:
        assert 41.860000 <= stop.latitude <= 41.900000
        assert -87.660000 <= stop.longitude <= -87.600000
