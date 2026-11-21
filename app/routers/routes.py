from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.route import RouteRead
from app.services import route_service

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("", response_model=list[RouteRead])
def read_routes(db: Session = Depends(get_db)):
    return route_service.list_routes(db)
