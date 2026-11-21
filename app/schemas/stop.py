from pydantic import BaseModel, ConfigDict


class StopRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stop_id: int
    name: str
    latitude: float
    longitude: float
    address: str | None = None
