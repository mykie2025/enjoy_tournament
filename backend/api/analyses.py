from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..database.database import get_db
from ..database.models import Analysis, Match, User, Recommendation

# Models
class AnalysisBase(BaseModel):
    user_id: int
    match_id: int
    title: str
    content: str
    tournament_info: Optional[dict] = None
    skill_coach: Optional[dict] = None
    orchestrator: Optional[dict] = None

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisResponse(AnalysisBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

class RecommendationResponse(BaseModel):
    id: int
    analysis_id: int
    title: str
    description: str
    category: str
    priority: int
    completed: bool
    
    class Config:
        orm_mode = True
        from_attributes = True

class AnalysisDetail(AnalysisResponse):
    recommendations: List[RecommendationResponse] = []
    
    class Config:
        orm_mode = True
        from_attributes = True

# Router
router = APIRouter(
    prefix="/analyses",
    tags=["analyses"],
    responses={404: {"description": "Not found"}}
)

# Endpoints
@router.get("/", response_model=List[AnalysisResponse])
def get_analyses(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    match_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get all analyses with optional filtering
    """
    query = db.query(Analysis)
    
    if user_id:
        query = query.filter(Analysis.user_id == user_id)
    
    if match_id:
        query = query.filter(Analysis.match_id == match_id)
    
    analyses = query.offset(skip).limit(limit).all()
    return analyses

@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(analysis: AnalysisCreate, db: Session = Depends(get_db)):
    """
    Create a new analysis
    """
    # Verify match exists
    match = db.query(Match).filter(Match.id == analysis.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Verify user exists
    user = db.query(User).filter(User.id == analysis.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_analysis = Analysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@router.get("/{analysis_id}", response_model=AnalysisDetail)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get a specific analysis by ID with its recommendations
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.put("/{analysis_id}", response_model=AnalysisResponse)
def update_analysis(analysis_id: int, analysis: AnalysisCreate, db: Session = Depends(get_db)):
    """
    Update an analysis
    """
    db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Verify match exists
    match = db.query(Match).filter(Match.id == analysis.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Verify user exists
    user = db.query(User).filter(User.id == analysis.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in analysis.dict().items():
        setattr(db_analysis, key, value)
    
    # Update the updated_at timestamp
    db_analysis.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Delete an analysis
    """
    db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    db.delete(db_analysis)
    db.commit()
    return {"success": True}

@router.get("/{analysis_id}/recommendations", response_model=List[RecommendationResponse])
def get_analysis_recommendations(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get all recommendations for a specific analysis
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis.recommendations
