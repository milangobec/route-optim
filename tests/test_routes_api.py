from app.models import Route, RouteStop, Stop


def test_get_routes_returns_empty_list_when_none_exist(client):
    response = client.get("/routes")

    assert response.status_code == 200
    assert response.json() == []


def test_get_routes_returns_route_with_no_stops(client, db_session):
    db_session.add(Route(name="Empty Route"))
    db_session.commit()

    response = client.get("/routes")

    body = response.json()
    assert len(body) == 1
    assert body[0]["name"] == "Empty Route"
    assert body[0]["route_stops"] == []
    assert set(body[0].keys()) == {"route_id", "name", "created_date", "route_stops"}


def test_get_routes_returns_nested_stops_in_input_order(client, db_session):
    depot = Stop(name="Depot", latitude=41.8781, longitude=-87.6298)
    stop_a = Stop(name="Stop A", latitude=41.852291, longitude=-87.654357)
    stop_b = Stop(name="Stop B", latitude=41.873571, longitude=-87.610189)
    route = Route(name="Tuesday Deliveries")
    db_session.add_all([depot, stop_a, stop_b, route])
    db_session.commit()

    db_session.add_all(
        [
            RouteStop(route_id=route.route_id, stop_id=stop_b.stop_id, input_order=2),
            RouteStop(route_id=route.route_id, stop_id=depot.stop_id, input_order=0),
            RouteStop(route_id=route.route_id, stop_id=stop_a.stop_id, input_order=1),
        ]
    )
    db_session.commit()

    response = client.get("/routes")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    route_stops = body[0]["route_stops"]
    assert [rs["input_order"] for rs in route_stops] == [0, 1, 2]
    assert [rs["stop"]["name"] for rs in route_stops] == ["Depot", "Stop A", "Stop B"]
    assert all(rs["optimized_order"] is None for rs in route_stops)
    assert route_stops[1]["stop"]["latitude"] == 41.852291
