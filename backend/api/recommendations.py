from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..database.database import get_db
from ..database.models import Recommendation, Analysis

# Models
class RecommendationBase(BaseModel):
    analysis_id: int
    title: str
    description: str
    category: str
    priority: int
    completed: bool = False

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationResponse(RecommendationBase):
    id: int
    
    class Config:
        orm_mode = True

class RecommendationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None

# Router
router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
    responses={404: {"description": "Not found"}}
)

# Endpoints
@router.put("/{recommendation_id}", response_model=RecommendationResponse)
def update_recommendation(recommendation_id: int, recommendation: RecommendationUpdate, db: Session = Depends(get_db)):
    """
    Update a recommendation
    """
    db_recommendation = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if db_recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Update only provided fields
    update_data = recommendation.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recommendation, key, value)
    
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation

@router.put("/{recommendation_id}/complete", response_model=RecommendationResponse)
def complete_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    """
    Mark a recommendation as complete
    """
    db_recommendation = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if db_recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    db_recommendation.completed = True
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation
