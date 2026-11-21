from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Route, RouteStop


def list_routes(db: Session) -> list[Route]:
    statement = (
        select(Route)
        .options(selectinload(Route.route_stops).selectinload(RouteStop.stop))
        .order_by(Route.route_id)
    )
    return list(db.scalars(statement))
