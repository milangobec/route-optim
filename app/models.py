from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Stop(Base):
    __tablename__ = "stops"

    stop_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str | None] = mapped_column(String, nullable=True)

    route_stops: Mapped[list["RouteStop"]] = relationship(back_populates="stop")


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    route_stops: Mapped[list["RouteStop"]] = relationship(
        back_populates="route",
        cascade="all, delete-orphan",
        order_by="RouteStop.input_order",
    )


class RouteStop(Base):
    __tablename__ = "route_stops"
    __table_args__ = (
        UniqueConstraint("route_id", "stop_id", name="uq_route_stop"),
        UniqueConstraint("route_id", "input_order", name="uq_route_input_order"),
    )

    route_stop_id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False
    )
    stop_id: Mapped[int] = mapped_column(ForeignKey("stops.stop_id"), nullable=False)
    input_order: Mapped[int] = mapped_column(nullable=False)
    optimized_order: Mapped[int | None] = mapped_column(nullable=True)

    route: Mapped["Route"] = relationship(back_populates="route_stops")
    stop: Mapped["Stop"] = relationship(back_populates="route_stops")
