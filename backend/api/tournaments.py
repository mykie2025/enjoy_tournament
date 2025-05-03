from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from ..database.database import get_db
from ..database.models import Tournament, Match

# Models
class TournamentBase(BaseModel):
    name: str
    location: str
    start_date: datetime
    end_date: datetime
    surface: str
    category: str

class TournamentCreate(TournamentBase):
    pass

class TournamentResponse(TournamentBase):
    id: int
    
    class Config:
        orm_mode = True

class TournamentDetail(TournamentResponse):
    matches: List = []
    
    class Config:
        orm_mode = True

# Router
router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"],
    responses={404: {"description": "Not found"}}
)

# Endpoints
@router.get("/", response_model=List[TournamentResponse])
def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all tournaments with pagination
    """
    tournaments = db.query(Tournament).offset(skip).limit(limit).all()
    return tournaments

@router.post("/", response_model=TournamentResponse, status_code=status.HTTP_201_CREATED)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    """
    Create a new tournament
    """
    db_tournament = Tournament(**tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@router.get("/{tournament_id}", response_model=TournamentDetail)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Get a specific tournament by ID with its matches
    """
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

@router.put("/{tournament_id}", response_model=TournamentResponse)
def update_tournament(tournament_id: int, tournament: TournamentCreate, db: Session = Depends(get_db)):
    """
    Update a tournament
    """
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    for key, value in tournament.dict().items():
        setattr(db_tournament, key, value)
    
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@router.delete("/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Delete a tournament
    """
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    db.delete(db_tournament)
    db.commit()
    return {"success": True}

@router.get("/{tournament_id}/matches", response_model=List)
def get_tournament_matches(tournament_id: int, db: Session = Depends(get_db)):
    """
    Get all matches for a specific tournament
    """
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    return tournament.matches
