from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..database.database import get_db
from ..database.models import Point, Match

# Models
class PointBase(BaseModel):
    match_id: int
    point_number: int
    game_score: str
    point_score: str
    server: str
    winner: str
    first_serve_in: Optional[bool] = None
    serve_type: Optional[str] = None
    return_type: Optional[str] = None
    rally_length: Optional[int] = None
    winning_shot: Optional[str] = None

class PointCreate(PointBase):
    pass

class PointResponse(PointBase):
    id: int
    
    class Config:
        orm_mode = True

# Router
router = APIRouter(
    prefix="/points",
    tags=["points"],
    responses={404: {"description": "Not found"}}
)

# Endpoints
@router.get("/{point_id}", response_model=PointResponse)
def get_point(point_id: int, db: Session = Depends(get_db)):
    """
    Get a specific point by ID
    """
    point = db.query(Point).filter(Point.id == point_id).first()
    if point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    return point

@router.put("/{point_id}", response_model=PointResponse)
def update_point(point_id: int, point: PointCreate, db: Session = Depends(get_db)):
    """
    Update a point
    """
    db_point = db.query(Point).filter(Point.id == point_id).first()
    if db_point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    
    # Verify match exists
    match = db.query(Match).filter(Match.id == point.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    for key, value in point.dict().items():
        setattr(db_point, key, value)
    
    db.commit()
    db.refresh(db_point)
    return db_point

@router.delete("/{point_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_point(point_id: int, db: Session = Depends(get_db)):
    """
    Delete a point
    """
    db_point = db.query(Point).filter(Point.id == point_id).first()
    if db_point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    
    db.delete(db_point)
    db.commit()
    return {"success": True}
