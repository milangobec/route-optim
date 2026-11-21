from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.stop import StopRead
from app.services import stop_service

router = APIRouter(prefix="/stops", tags=["stops"])


@router.get("", response_model=list[StopRead])
def read_stops(db: Session = Depends(get_db)):
    return stop_service.list_stops(db)
