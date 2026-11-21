import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Route, RouteStop, Stop


def test_stop_route_link_via_routestop(db_session):
    stop = Stop(name="Depot", latitude=41.8781, longitude=-87.6298)
    route = Route(name="Tuesday Deliveries")
    db_session.add_all([stop, route])
    db_session.commit()

    link = RouteStop(route_id=route.route_id, stop_id=stop.stop_id, input_order=0)
    db_session.add(link)
    db_session.commit()

    db_session.refresh(route)
    db_session.refresh(stop)

    assert route.route_stops[0].stop.name == "Depot"
    assert stop.route_stops[0].route.name == "Tuesday Deliveries"


def test_routestop_rejects_nonexistent_stop_id(db_session):
    route = Route(name="Weekend Errands")
    db_session.add(route)
    db_session.commit()

    bad_link = RouteStop(route_id=route.route_id, stop_id=9999, input_order=0)
    db_session.add(bad_link)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_duplicate_stop_in_same_route_rejected(db_session):
    stop = Stop(name="Stop A", latitude=41.85, longitude=-87.65)
    route = Route(name="Fundraiser Drop-offs")
    db_session.add_all([stop, route])
    db_session.commit()

    db_session.add(RouteStop(route_id=route.route_id, stop_id=stop.stop_id, input_order=0))
    db_session.commit()

    db_session.add(RouteStop(route_id=route.route_id, stop_id=stop.stop_id, input_order=1))

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_duplicate_input_order_in_same_route_rejected(db_session):
    stop_a = Stop(name="Stop A", latitude=41.85, longitude=-87.65)
    stop_b = Stop(name="Stop B", latitude=41.87, longitude=-87.61)
    route = Route(name="Weekday Round")
    db_session.add_all([stop_a, stop_b, route])
    db_session.commit()

    db_session.add(RouteStop(route_id=route.route_id, stop_id=stop_a.stop_id, input_order=0))
    db_session.commit()

    db_session.add(RouteStop(route_id=route.route_id, stop_id=stop_b.stop_id, input_order=0))

    with pytest.raises(IntegrityError):
        db_session.commit()
