from app.models import Stop


def test_get_stops_returns_empty_list_when_none_exist(client):
    response = client.get("/stops")

    assert response.status_code == 200
    assert response.json() == []


def test_get_stops_returns_seeded_stops_in_id_order(client, db_session):
    db_session.add_all(
        [
            Stop(name="Depot", latitude=41.8781, longitude=-87.6298),
            Stop(
                name="Stop A",
                latitude=41.852291,
                longitude=-87.654357,
                address="1 Main St",
            ),
        ]
    )
    db_session.commit()

    response = client.get("/stops")

    assert response.status_code == 200
    body = response.json()
    assert [stop["name"] for stop in body] == ["Depot", "Stop A"]
    assert body[0]["address"] is None
    assert body[1]["address"] == "1 Main St"
    assert set(body[0].keys()) == {
        "stop_id",
        "name",
        "latitude",
        "longitude",
        "address",
    }
    assert body[0]["latitude"] == 41.8781
    assert body[0]["longitude"] == -87.6298
