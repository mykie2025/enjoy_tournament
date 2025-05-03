from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, date, timedelta
import os
import logging

from ..database.database import get_db
from ..database.models import Tournament, Match
from ..data_sources.sportradar_api_source import SportRadarAPISource

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models
class TournamentBase(BaseModel):
    name: str
    location: str
    start_date: datetime
    end_date: datetime
    surface: str
    category: str

class TournamentCreate(TournamentBase):
    external_id: str = None
    is_selected: bool = False
    status: str = "upcoming"

class TournamentResponse(TournamentBase):
    id: int
    external_id: str = None
    is_selected: bool = False
    status: str = "upcoming"
    
    class Config:
        orm_mode = True

class TournamentDetail(TournamentResponse):
    matches: List = []
    
    class Config:
        orm_mode = True

# Request models for multiple tournament selection
class TournamentIdsRequest(BaseModel):
    tournament_ids: List[str]

class UpdateExternalIdRequest(BaseModel):
    tournament_id: int
    external_id: str

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
                tournament_id = season.get('id')
                tournament_name = season.get('name')
                tournament_year = season.get('year')
                competition_id = season.get('competition_id') or tournament_id
                
                # Get start and end dates if available
                start_date = None
                end_date = None
                
                if 'start_date' in season and season['start_date']:
                    try:
                        start_date = datetime.strptime(season['start_date'], "%Y-%m-%d").date()
                    except (ValueError, TypeError):
                        pass
                        
                if 'end_date' in season and season['end_date']:
                    try:
                        end_date = datetime.strptime(season['end_date'], "%Y-%m-%d").date()
                    except (ValueError, TypeError):
                        pass
                
                # Determine tournament status based on dates
                status = "upcoming"
                if start_date and end_date:
                    if current_date < start_date:
                        status = "upcoming"
                    elif current_date > end_date:
                        status = "ended"
                    else:
                        status = "live"
                
                # Create or update tournament entry
                if competition_id not in tournaments:
                    tournaments[competition_id] = {
                        'id': competition_id,
                        'external_id': competition_id,
                        'name': tournament_name,
                        'year': tournament_year,
                        'start_date': season.get('start_date'),
                        'end_date': season.get('end_date'),
                        'status': status,
                        'match_count': 0,
                        'category': season.get('category', {}).get('name') if 'category' in season else None,
                        'season_ids': [tournament_id]
                    }
                else:
                    # Update existing tournament with additional season info
                    if tournament_id not in tournaments[competition_id]['season_ids']:
                        tournaments[competition_id]['season_ids'].append(tournament_id)
                    
                    # Update dates if current tournament has more specific dates
                    if start_date and (not tournaments[competition_id].get('start_date') or 
                                     (tournaments[competition_id].get('start_date') and 
                                      start_date < datetime.strptime(tournaments[competition_id]['start_date'], "%Y-%m-%d").date())):
                        tournaments[competition_id]['start_date'] = season.get('start_date')
                    
                    if end_date and (not tournaments[competition_id].get('end_date') or 
                                   (tournaments[competition_id].get('end_date') and 
                                    end_date > datetime.strptime(tournaments[competition_id]['end_date'], "%Y-%m-%d").date())):
                        tournaments[competition_id]['end_date'] = season.get('end_date')
                    
                    # Update status based on dates
                    if status == "live":
                        tournaments[competition_id]['status'] = "live"
        
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

@router.post("/select/{external_id}", response_model=Dict[str, Any])
def select_tournament(external_id: str, db: Session = Depends(get_db)):
    """
    Select a tournament to save to the database
    """
    try:
        # Check if tournament already exists in database
        db_tournament = db.query(Tournament).filter(Tournament.external_id == external_id).first()
        
        if db_tournament:
            # Update existing tournament
            db_tournament.is_selected = True
            db.commit()
            db.refresh(db_tournament)
            return {"status": "success", "message": f"Tournament '{db_tournament.name}' selected successfully", "data": db_tournament}
        
        # Tournament doesn't exist, fetch from SportRadar
        seasons_data = sportradar_api._make_request("en/seasons.json")
        
        # Find the tournament in seasons data
        tournament_data = None
        for season in seasons_data.get('seasons', []):
            if season.get('id') == external_id or season.get('competition_id') == external_id:
                tournament_data = season
                break
        
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament with ID {external_id} not found"
            )
        
        # Determine tournament status based on dates
        current_date = datetime.now().date()
        status = "upcoming"
        
        start_date = None
        if 'start_date' in tournament_data and tournament_data['start_date']:
            try:
                start_date = datetime.strptime(tournament_data['start_date'], "%Y-%m-%d")
            except (ValueError, TypeError):
                start_date = datetime.now()
        else:
            start_date = datetime.now()
            
        end_date = None
        if 'end_date' in tournament_data and tournament_data['end_date']:
            try:
                end_date = datetime.strptime(tournament_data['end_date'], "%Y-%m-%d")
            except (ValueError, TypeError):
                end_date = start_date + timedelta(days=7)
        else:
            end_date = start_date + timedelta(days=7)
        
        if current_date < start_date.date():
            status = "upcoming"
        elif current_date > end_date.date():
            status = "ended"
        else:
            status = "live"
        
        # Create new tournament
        new_tournament = Tournament(
            name=tournament_data.get('name', 'Unknown Tournament'),
            location=tournament_data.get('category', {}).get('name', 'Unknown Location'),
            start_date=start_date,
            end_date=end_date,
            surface=tournament_data.get('surface', 'Unknown'),
            category=tournament_data.get('category', {}).get('name', 'Unknown'),
            external_id=external_id,
            is_selected=True,
            status=status
        )
        
        db.add(new_tournament)
        db.commit()
        db.refresh(new_tournament)
        
        return {"status": "success", "message": f"Tournament '{new_tournament.name}' selected and saved", "data": new_tournament}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error selecting tournament: {str(e)}"
        )

@router.post("/deselect/{external_id}", response_model=Dict[str, Any])
def deselect_tournament(external_id: str, db: Session = Depends(get_db)):
    """
    Deselect a tournament
    """
    try:
        # Find tournament in database
        db_tournament = db.query(Tournament).filter(Tournament.external_id == external_id).first()
        
        if not db_tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament with ID {external_id} not found"
            )
        
        # Update tournament
        db_tournament.is_selected = False
        db.commit()
        
        return {"status": "success", "message": f"Tournament '{db_tournament.name}' deselected successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deselecting tournament: {str(e)}"
        )

@router.get("/selected", response_model=Dict[str, Any])
def get_selected_tournaments(db: Session = Depends(get_db)):
    """
    Get all selected tournaments
    """
    try:
        logger.info("Fetching selected tournaments from database")
        # Get all selected tournaments
        selected_tournaments = db.query(Tournament).filter(Tournament.is_selected == True).all()
        logger.info(f"Found {len(selected_tournaments)} selected tournaments")
        
        # Convert SQLAlchemy objects to dictionaries
        result = []
        for t in selected_tournaments:
            result.append({
                "id": str(t.id),
                "name": t.name,
                "category": t.category,
                "status": t.status,
                "match_count": 0,
                "start_date": t.start_date.isoformat() if t.start_date else None,
                "end_date": t.end_date.isoformat() if t.end_date else None,
                "external_id": t.external_id,
                "is_selected": bool(t.is_selected)
            })
        
        return {"status": "success", "data": {"tournaments": result}}
    except Exception as e:
        logger.error(f"Error fetching selected tournaments: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching selected tournaments: {str(e)}"
        )

@router.get("/selected/ended", response_model=Dict[str, Any])
def get_ended_selected_tournaments(db: Session = Depends(get_db)):
    """
    Get all ended selected tournaments
    """
    try:
        # Get all ended selected tournaments
        ended_tournaments = db.query(Tournament).filter(
            Tournament.is_selected == True,
            Tournament.status == "ended"
        ).all()
        
        # Convert SQLAlchemy objects to dictionaries
        result = []
        for t in ended_tournaments:
            result.append({
                "id": str(t.id),
                "name": t.name,
                "category": t.category,
                "status": t.status,
                "match_count": 0,
                "start_date": t.start_date.isoformat() if t.start_date else None,
                "end_date": t.end_date.isoformat() if t.end_date else None,
                "external_id": t.external_id,
                "is_selected": bool(t.is_selected)
            })
        
        return {"status": "success", "data": {"tournaments": result}}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching ended tournaments: {str(e)}"
        )

@router.put("/update-status", response_model=Dict[str, Any])
def update_tournament_statuses(db: Session = Depends(get_db)):
    """
    Update the status of all tournaments based on their dates
    """
    try:
        # Get all tournaments
        tournaments = db.query(Tournament).all()
        current_date = datetime.now().date()
        updated_count = 0
        
        for tournament in tournaments:
            old_status = tournament.status
            
            # Determine status based on dates
            if current_date < tournament.start_date.date():
                new_status = "upcoming"
            elif current_date > tournament.end_date.date():
                new_status = "ended"
            else:
                new_status = "live"
            
            if old_status != new_status:
                tournament.status = new_status
                updated_count += 1
        
        db.commit()
        
        return {
            "status": "success", 
            "message": f"Updated status for {updated_count} tournaments",
            "data": {"updated_count": updated_count}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating tournament statuses: {str(e)}"
        )

@router.post("/select-multiple", response_model=Dict[str, Any])
def select_multiple_tournaments(request: TournamentIdsRequest, db: Session = Depends(get_db)):
    """
    Select multiple tournaments to save to the database
    """
    try:
        tournament_ids = request.tournament_ids
        if not tournament_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No tournament IDs provided"
            )
        
        # Get all tournaments from SportRadar
        seasons_data = sportradar_api._make_request("en/seasons.json")
        
        # Extract unique tournaments from seasons data
        tournaments_data = {}
        current_date = datetime.now().date()
        
        # Process seasons data to extract tournament information
        for season in seasons_data.get("seasons", []):
            # Use the same external_id format as your database and frontend
            external_id = season.get("competition_id") or season.get("id") or season.get("tournament_id")
            if external_id:
                if external_id not in tournaments_data:
                    name = season.get("tournament", {}).get("name", "Unknown Tournament")
                    year = season.get("year", "")
                    start_date_str = season.get("start_date")
                    end_date_str = season.get("end_date")
                    if start_date_str and end_date_str:
                        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                        status = "upcoming"
                        if current_date < start_date.date():
                            status = "upcoming"
                        elif current_date > end_date.date():
                            status = "ended"
                        else:
                            status = "live"
                        tournaments_data[external_id] = {
                            "id": external_id,
                            "name": name,
                            "year": year,
                            "start_date": start_date,
                            "end_date": end_date,
                            "status": status,
                            "category": season.get("tournament", {}).get("category", {}).get("name", "Tennis"),
                            "external_id": external_id
                        }
        
        logger.info(f"Processing tournament IDs: {tournament_ids}")
        logger.info(f"Checking against {len(tournaments_data)} tournaments found in SportRadar seasons.json")
        
        selected_count = 0
        not_found = []
        
        for external_id in tournament_ids:
            logger.debug(f"Processing external_id: {external_id}")
            # Check if tournament exists in database
            db_tournament = db.query(Tournament).filter(Tournament.external_id == external_id).first()
            
            if db_tournament:
                logger.debug(f"  Found existing tournament in DB (ID: {db_tournament.id})")
                # Update existing tournament
                if not db_tournament.is_selected:
                    logger.debug(f"    Marking DB tournament as selected.")
                    db_tournament.is_selected = True
                    selected_count += 1
                else:
                    logger.debug(f"    DB tournament already marked as selected.")
            else:
                logger.debug(f"  Tournament not found in DB with external_id: {external_id}")
                # Check if tournament exists in SportRadar data
                if external_id in tournaments_data:
                    logger.debug(f"  Found tournament in fresh SportRadar data.")
                    tournament_data = tournaments_data[external_id]
                    
                    # Create new tournament
                    logger.debug(f"    Creating new tournament record in DB and marking as selected.")
                    new_tournament = Tournament(
                        name=tournament_data["name"],
                        location="Unknown",  # SportRadar doesn't provide location directly
                        start_date=tournament_data["start_date"],
                        end_date=tournament_data["end_date"],
                        surface="Unknown",  # SportRadar doesn't provide surface directly
                        category=tournament_data["category"],
                        external_id=tournament_data["external_id"],
                        is_selected=True,
                        status=tournament_data["status"]
                    )
                    
                    db.add(new_tournament)
                    selected_count += 1
                else:
                    logger.debug(f"  Tournament not found in fresh SportRadar data either.")
                    not_found.append(external_id)
        
        logger.info(f"Finished processing. Selected count: {selected_count}, Not found count: {len(not_found)}")
        db.commit()
        
        return {
            "status": "success",
            "message": f"Selected {selected_count} tournaments",
            "data": {
                "selected_count": selected_count,
                "not_found": not_found
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error in select_multiple_tournaments: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error selecting tournaments: {str(e)}"
        )

@router.post("/deselect-multiple", response_model=Dict[str, Any])
def deselect_multiple_tournaments(request: TournamentIdsRequest, db: Session = Depends(get_db)):
    """
    Deselect multiple tournaments
    """
    try:
        tournament_ids = request.tournament_ids
        if not tournament_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No tournament IDs provided"
            )
        
        # Process each tournament ID
        deselected_count = 0
        not_found = []
        
        for external_id in tournament_ids:
            # Check if tournament exists in database
            db_tournament = db.query(Tournament).filter(Tournament.external_id == external_id).first()
            
            if db_tournament:
                # Update existing tournament
                if db_tournament.is_selected:
                    db_tournament.is_selected = False
                    deselected_count += 1
            else:
                not_found.append(external_id)
        
        db.commit()
        
        return {
            "status": "success",
            "message": f"Deselected {deselected_count} tournaments",
            "data": {
                "deselected_count": deselected_count,
                "not_found": not_found
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deselecting tournaments: {str(e)}"
        )

@router.post("/debug/update-external-id", response_model=Dict[str, Any])
def debug_update_external_id(request: UpdateExternalIdRequest, db: Session = Depends(get_db)):
    """
    DEBUGGING ENDPOINT: Update the external_id for an existing tournament.
    REMOVE LATER.
    """
    logger.info(f"DEBUG: Updating external_id for tournament ID {request.tournament_id} to {request.external_id}")
    try:
        # Find the tournament by ID
        tournament = db.query(Tournament).filter(Tournament.id == request.tournament_id).first()
        
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament with ID {request.tournament_id} not found"
            )
        
        # Update the external_id
        tournament.external_id = request.external_id
        db.commit()
        
        logger.info(f"DEBUG: Successfully updated external_id for tournament {tournament.name}")
        return {
            "status": "success",
            "message": f"Updated external_id for tournament {tournament.name}",
            "data": {
                "id": tournament.id,
                "name": tournament.name,
                "external_id": tournament.external_id
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating external_id: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating external_id: {str(e)}"
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
