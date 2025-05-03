from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, date, timedelta
import os

from ..database.database import get_db
from ..database.models import Tournament, Match
from ..data_sources.sportradar_api_source import SportRadarAPISource

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

# Add SportRadar API source
sportradar_api = SportRadarAPISource()

# Endpoints
@router.get("/", response_model=List[TournamentResponse])
def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all tournaments with pagination
    """
    tournaments = db.query(Tournament).offset(skip).limit(limit).all()
    return tournaments

@router.get("/api/live", response_model=Dict[str, Any])
def get_live_tournaments():
    """
    Get all currently live tournaments from SportRadar
    """
    try:
        # Get live tournaments from SportRadar
        live_data = sportradar_api.get_current_tournaments()
        return {"status": "success", "data": live_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching live tournaments: {str(e)}"
        )

@router.get("/api/daily/{date_str}", response_model=Dict[str, Any])
def get_daily_schedule(date_str: str):
    """
    Get tournament schedule for a specific date from SportRadar
    Format: YYYY-MM-DD
    """
    try:
        # Validate date format
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
            
        # Get daily schedule from SportRadar
        daily_data = sportradar_api.get_daily_summaries(date_str)
        return {"status": "success", "data": daily_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching daily schedule: {str(e)}"
        )

@router.get("/api/today", response_model=Dict[str, Any])
def get_today_schedule():
    """
    Get tournament schedule for today from SportRadar
    """
    try:
        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get daily schedule from SportRadar
        daily_data = sportradar_api.get_daily_summaries(today)
        return {"status": "success", "data": daily_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching today's schedule: {str(e)}"
        )

@router.get("/api/all", response_model=Dict[str, Any])
def get_all_tournaments():
    """
    Get all available tournaments from SportRadar
    """
    try:
        # Get seasons data which contains tournament information
        seasons_data = sportradar_api._make_request("en/seasons.json")
        print("Seasons data fetched successfully")
        
        # Extract unique tournaments from seasons data
        tournaments = {}
        current_date = datetime.now().date()
        
        # Process seasons data
        if seasons_data and 'seasons' in seasons_data:
            for season in seasons_data['seasons']:
                # Extract tournament info
                start_date = datetime.strptime(season.get('start_date', '2000-01-01'), '%Y-%m-%d').date()
                end_date = datetime.strptime(season.get('end_date', '2000-01-01'), '%Y-%m-%d').date()
                
                # Only include current or upcoming tournaments (within 7 days)
                if end_date >= current_date and start_date <= current_date + timedelta(days=7):
                    # Create a unique tournament ID based on the competition ID
                    competition_id = season.get('competition_id')
                    if competition_id:
                        # Use competition_id as the tournament identifier
                        if competition_id not in tournaments:
                            tournaments[competition_id] = {
                                'id': competition_id,
                                'name': season.get('name', 'Unknown Tournament'),
                                'start_date': season.get('start_date'),
                                'end_date': season.get('end_date'),
                                'year': season.get('year'),
                                'status': 'live' if start_date <= current_date <= end_date else 'upcoming',
                                'season_ids': [season.get('id')],  # Store all related season IDs
                                'match_count': 0
                            }
                        else:
                            # Add this season ID to the existing tournament
                            tournaments[competition_id]['season_ids'].append(season.get('id'))
        
        print(f"Found {len(tournaments)} tournaments from seasons data")
        
        # Get live data to identify currently active tournaments
        live_data = sportradar_api.get_current_tournaments()
        
        # Update tournament status and match count based on live data
        if live_data and 'sport_events' in live_data:
            for event in live_data['sport_events']:
                if 'tournament' in event:
                    tournament = event['tournament']
                    tournament_id = tournament.get('id')
                    competition_id = tournament.get('category', {}).get('id') or tournament_id
                    
                    if competition_id in tournaments:
                        # Update existing tournament
                        tournaments[competition_id]['status'] = 'live'
                        tournaments[competition_id]['match_count'] += 1
                    else:
                        # Add new tournament from live data
                        tournaments[competition_id] = {
                            'id': competition_id,
                            'name': tournament.get('name', 'Unknown Tournament'),
                            'category': tournament.get('category', {}).get('name', 'Unknown'),
                            'status': 'live',
                            'match_count': 1,
                            'season_ids': []
                        }
        
        # Get today's schedule to update match counts
        today = datetime.now().strftime("%Y-%m-%d")
        daily_data = sportradar_api.get_daily_summaries(today)
        
        if daily_data and 'sport_events' in daily_data:
            for event in daily_data['sport_events']:
                if 'tournament' in event:
                    tournament = event['tournament']
                    tournament_id = tournament.get('id')
                    competition_id = tournament.get('category', {}).get('id') or tournament_id
                    
                    if competition_id in tournaments:
                        # Update match count for existing tournament
                        tournaments[competition_id]['match_count'] += 1
        
        # Convert dictionary to list
        tournament_list = list(tournaments.values())
        
        # Sort tournaments: live first, then by match count, then by start date
        tournament_list.sort(key=lambda x: (
            0 if x['status'] == 'live' else 1,
            -x.get('match_count', 0),
            x.get('start_date', '9999-12-31')
        ))
        
        # Limit to the top 20 tournaments for better UI performance
        tournament_list = tournament_list[:20]
        
        print(f"Returning {len(tournament_list)} tournaments")
        for t in tournament_list:
            print(f"Tournament: {t['name']} - {t['status']} - {t.get('match_count', 0)} matches")
        
        return {"status": "success", "data": {"tournaments": tournament_list}}
    except Exception as e:
        print(f"Error in get_all_tournaments: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tournaments: {str(e)}"
        )

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
