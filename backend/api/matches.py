from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..database.database import get_db
from ..database.models import Match, Tournament, Point

# Models
class MatchBase(BaseModel):
    tournament_id: int
    round: str
    player1: str
    player2: str
    score: str
    date: datetime
    duration: int

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: int
    
    class Config:
        orm_mode = True

class MatchDetail(MatchResponse):
    points: List = []
    
    class Config:
        orm_mode = True

# Router
router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    responses={404: {"description": "Not found"}}
)

# Endpoints
@router.get("/", response_model=List[MatchResponse])
def get_matches(
    skip: int = 0, 
    limit: int = 100, 
    tournament_id: Optional[int] = None,
    player: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all matches with optional filtering
    """
    query = db.query(Match)
    
    if tournament_id:
        query = query.filter(Match.tournament_id == tournament_id)
    
    if player:
        query = query.filter(
            (Match.player1.contains(player)) | (Match.player2.contains(player))
        )
    
    matches = query.offset(skip).limit(limit).all()
    return matches

@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    """
    Create a new match
    """
    # Verify tournament exists
    tournament = db.query(Tournament).filter(Tournament.id == match.tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    db_match = Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

@router.get("/{match_id}", response_model=MatchDetail)
def get_match(match_id: int, db: Session = Depends(get_db)):
    """
    Get a specific match by ID with its points
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.put("/{match_id}", response_model=MatchResponse)
def update_match(match_id: int, match: MatchCreate, db: Session = Depends(get_db)):
    """
    Update a match
    """
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Verify tournament exists
    tournament = db.query(Tournament).filter(Tournament.id == match.tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    for key, value in match.dict().items():
        setattr(db_match, key, value)
    
    db.commit()
    db.refresh(db_match)
    return db_match

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    """
    Delete a match
    """
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    db.delete(db_match)
    db.commit()
    return {"success": True}

@router.get("/{match_id}/points", response_model=List)
def get_match_points(match_id: int, db: Session = Depends(get_db)):
    """
    Get all points for a specific match
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return match.points

@router.post("/{match_id}/points", status_code=status.HTTP_201_CREATED)
def add_point_to_match(match_id: int, point_data: dict, db: Session = Depends(get_db)):
    """
    Add a point to a match
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Create point with match_id
    point_data["match_id"] = match_id
    new_point = Point(**point_data)
    
    db.add(new_point)
    db.commit()
    db.refresh(new_point)
    
    return new_point
