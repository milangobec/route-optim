from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.stop import StopRead


class RouteStopRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    input_order: int
    optimized_order: int | None = None
    stop: StopRead


class RouteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    route_id: int
    name: str
    created_date: datetime
    route_stops: list[RouteStopRead]
