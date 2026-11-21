import random

import pytest

from app.engine.types import Coordinate


@pytest.fixture()
def db_session():
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from app.database import Base

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


BOUNDING_BOX = {
    "min_lat": 41.860000,
    "max_lat": 41.900000,
    "min_lon": -87.660000,
    "max_lon": -87.600000,
}


@pytest.fixture()
def worked_example_stops():
    return [
        Coordinate("Depot", 41.878100, -87.629800),
        Coordinate("A", 41.852291, -87.654357),
        Coordinate("B", 41.873571, -87.610189),
        Coordinate("C", 41.855528, -87.646406),
        Coordinate("D", 41.885746, -87.602937),
        Coordinate("E", 41.882726, -87.635999),
    ]


@pytest.fixture()
def square_stops():
    return [
        Coordinate("Depot", 41.878100, -87.629800),
        Coordinate("B", 41.878100, -87.619800),
        Coordinate("C", 41.868100, -87.619800),
        Coordinate("D", 41.868100, -87.629800),
    ]


@pytest.fixture()
def triangle_stops():
    return [
        Coordinate("Depot", 41.878100, -87.629800),
        Coordinate("A", 41.885000, -87.640000),
        Coordinate("B", 41.885000, -87.620000),
    ]


def generate_random_stops(count, bounding_box=BOUNDING_BOX, seed=None):
    rng = random.Random(seed)
    stops = [Coordinate("Depot", 41.878100, -87.629800)]
    for i in range(count):
        lat = rng.uniform(bounding_box["min_lat"], bounding_box["max_lat"])
        lon = rng.uniform(bounding_box["min_lon"], bounding_box["max_lon"])
        stops.append(Coordinate(f"Stop {i + 1}", lat, lon))
    return stops


@pytest.fixture()
def random_stops_factory():
    return generate_random_stops


@pytest.fixture()
def client(db_session):
    from fastapi.testclient import TestClient

    from app.database import get_db
    from app.main import app

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
