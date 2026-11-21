from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Route, RouteStop, Stop

WORKED_EXAMPLE = [
    ("Depot", 41.878100, -87.629800),
    ("A", 41.852291, -87.654357),
    ("B", 41.873571, -87.610189),
    ("C", 41.855528, -87.646406),
    ("D", 41.885746, -87.602937),
    ("E", 41.882726, -87.635999),
]


def seed() -> bool:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.scalars(select(Stop)).first() is not None:
            return False

        stops = [
            Stop(name=name, latitude=latitude, longitude=longitude)
            for name, latitude, longitude in WORKED_EXAMPLE
        ]
        route = Route(name="Worked Example")
        db.add_all(stops + [route])
        db.commit()

        for order, stop in enumerate(stops):
            db.add(
                RouteStop(
                    route_id=route.route_id, stop_id=stop.stop_id, input_order=order
                )
            )
        db.commit()
    return True


if __name__ == "__main__":
    if seed():
        print("Seeded the worked example: 6 stops and 1 route.")
    else:
        print("Stops already exist, nothing seeded.")
