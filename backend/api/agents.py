from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
import uuid
import json

from ..database.database import get_db
from ..database.models import Match, Analysis
from ..agents.orchestrator_agent import OrchestratorAgent
from ..agents.tournament_info_agent import TournamentInfoAgent
from ..agents.tennis_skill_coach_agent import TennisSkillCoachAgent

# Models
class AnalysisRequest(BaseModel):
    match_id: int
    user_id: int
    analysis_type: str  # 'full', 'tournament_info', 'skill_coach', 'orchestrator'

class JobStatus(BaseModel):
    job_id: str
    status: str  # 'pending', 'in_progress', 'completed', 'failed'
    progress: int  # 0-100
    result_id: Optional[int] = None
    error: Optional[str] = None

# Router
router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}}
)

# In-memory job storage (would be replaced with Redis or similar in production)
active_jobs = {}

# Helper functions
def run_analysis_job(job_id: str, match_id: int, user_id: int, analysis_type: str, db: Session):
    """
    Background task to run analysis
    """
    try:
        # Update job status
        active_jobs[job_id]["status"] = "in_progress"
        active_jobs[job_id]["progress"] = 10
        
        # Get match data
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            active_jobs[job_id]["status"] = "failed"
            active_jobs[job_id]["error"] = "Match not found"
            return
        
        # Create analysis record
        analysis = Analysis(
            user_id=user_id,
            match_id=match_id,
            title=f"Analysis of {match.player1} vs {match.player2}",
            content=""
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        active_jobs[job_id]["progress"] = 20
        
        # Run appropriate agent(s)
        if analysis_type in ["full", "tournament_info"]:
            active_jobs[job_id]["progress"] = 30
            tournament_info_agent = TournamentInfoAgent()
            tournament_info_results = tournament_info_agent.analyze_match(match_id)
            analysis.tournament_info = tournament_info_results
            db.commit()
            active_jobs[job_id]["progress"] = 50
        
        if analysis_type in ["full", "skill_coach"]:
            active_jobs[job_id]["progress"] = 60
            skill_coach_agent = TennisSkillCoachAgent()
            skill_coach_results = skill_coach_agent.analyze_match(match_id)
            analysis.skill_coach = skill_coach_results
            db.commit()
            active_jobs[job_id]["progress"] = 80
        
        if analysis_type in ["full", "orchestrator"]:
            active_jobs[job_id]["progress"] = 90
            orchestrator_agent = OrchestratorAgent()
            orchestrator_results = orchestrator_agent.analyze_match(match_id)
            analysis.orchestrator = orchestrator_results
            
            # Generate content summary from all agent outputs
            if analysis_type == "full":
                analysis.content = orchestrator_agent.generate_summary(
                    tournament_info=analysis.tournament_info,
                    skill_coach=analysis.skill_coach,
                    orchestrator=orchestrator_results
                )
            
            db.commit()
        
        # Update job status
        active_jobs[job_id]["status"] = "completed"
        active_jobs[job_id]["progress"] = 100
        active_jobs[job_id]["result_id"] = analysis.id
        
    except Exception as e:
        active_jobs[job_id]["status"] = "failed"
        active_jobs[job_id]["error"] = str(e)

# Endpoints
@router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
def analyze_match(
    analysis_request: AnalysisRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger a match analysis using the agent system
    """
    # Verify match exists
    match = db.query(Match).filter(Match.id == analysis_request.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Create job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    active_jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "result_id": None,
        "error": None
    }
    
    # Start background task
    background_tasks.add_task(
        run_analysis_job,
        job_id=job_id,
        match_id=analysis_request.match_id,
        user_id=analysis_request.user_id,
        analysis_type=analysis_request.analysis_type,
        db=db
    )
    
    return {"job_id": job_id}

@router.get("/status/{job_id}", response_model=JobStatus)
def get_job_status(job_id: str):
    """
    Check the status of an analysis job
    """
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_info = active_jobs[job_id]
    return {
        "job_id": job_id,
        "status": job_info["status"],
        "progress": job_info["progress"],
        "result_id": job_info["result_id"],
        "error": job_info["error"]
    }

@router.get("/orchestrator/{match_id}")
def get_orchestrator_insights(match_id: int, db: Session = Depends(get_db)):
    """
    Get orchestrator agent insights for a match
    """
    analysis = db.query(Analysis).filter(
        Analysis.match_id == match_id
    ).order_by(Analysis.created_at.desc()).first()
    
    if not analysis or not analysis.orchestrator:
        raise HTTPException(status_code=404, detail="Orchestrator analysis not found for this match")
    
    return analysis.orchestrator

@router.get("/tournament-info/{match_id}")
def get_tournament_info_insights(match_id: int, db: Session = Depends(get_db)):
    """
    Get tournament info agent insights for a match
    """
    analysis = db.query(Analysis).filter(
        Analysis.match_id == match_id
    ).order_by(Analysis.created_at.desc()).first()
    
    if not analysis or not analysis.tournament_info:
        raise HTTPException(status_code=404, detail="Tournament info analysis not found for this match")
    
    return analysis.tournament_info

@router.get("/skill-coach/{match_id}")
def get_skill_coach_insights(match_id: int, db: Session = Depends(get_db)):
    """
    Get skill coach agent insights for a match
    """
    analysis = db.query(Analysis).filter(
        Analysis.match_id == match_id
    ).order_by(Analysis.created_at.desc()).first()
    
    if not analysis or not analysis.skill_coach:
        raise HTTPException(status_code=404, detail="Skill coach analysis not found for this match")
    
    return analysis.skill_coach
