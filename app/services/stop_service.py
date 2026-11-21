from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Stop


def list_stops(db: Session) -> list[Stop]:
    return list(db.scalars(select(Stop).order_by(Stop.stop_id)))
