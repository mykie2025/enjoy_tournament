from typing import Dict, Any, Optional, List
import logging
from sqlalchemy.orm import Session

from .orchestrator_agent import OrchestratorAgent
from .tournament_info_agent import TournamentInfoAgent
from .tennis_skill_coach_agent import TennisSkillCoachAgent
from ..database.models import Match, Analysis, Recommendation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentManager:
    """
    Manager class for initializing and coordinating the agents in the system.
    Provides a simplified interface for using the agents.
    """
    
    def __init__(self):
        """Initialize the agent manager and all agent instances"""
        logger.info("Initializing AgentManager")
        self.orchestrator = OrchestratorAgent()
        self.tournament_info = TournamentInfoAgent()
        self.skill_coach = TennisSkillCoachAgent()
        logger.info("All agents initialized successfully")
    
    def analyze_match(self, match_id: int, user_id: int, db: Session) -> Analysis:
        """
        Perform a complete analysis of a match using all agents
        
        Args:
            match_id (int): ID of the match to analyze
            user_id (int): ID of the user requesting the analysis
            db (Session): Database session
            
        Returns:
            Analysis: The created analysis object
        """
        logger.info(f"Starting full match analysis for match_id={match_id}")
        
        # Get match data
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            logger.error(f"Match with id {match_id} not found")
            raise ValueError(f"Match with id {match_id} not found")
        
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
        
        logger.info(f"Created analysis record with id={analysis.id}")
        
        # Run tournament info agent
        logger.info("Running Tournament Info Agent")
        tournament_info_results = self.tournament_info.analyze_match(match_id)
        analysis.tournament_info = tournament_info_results
        db.commit()
        
        # Run skill coach agent
        logger.info("Running Tennis Skill Coach Agent")
        skill_coach_results = self.skill_coach.analyze_match(match_id)
        analysis.skill_coach = skill_coach_results
        db.commit()
        
        # Run orchestrator agent
        logger.info("Running Orchestrator Agent")
        orchestrator_results = self.orchestrator.analyze_match(match_id)
        analysis.orchestrator = orchestrator_results
        
        # Generate content summary
        logger.info("Generating analysis summary")
        analysis.content = self.orchestrator.generate_summary(
            tournament_info=analysis.tournament_info,
            skill_coach=analysis.skill_coach,
            orchestrator=orchestrator_results
        )
        
        # Generate recommendations
        logger.info("Generating recommendations")
        recommendations = self._generate_recommendations(analysis.id, orchestrator_results)
        
        # Save recommendations to database
        for rec in recommendations:
            db.add(rec)
        
        db.commit()
        db.refresh(analysis)
        
        logger.info(f"Analysis completed successfully, id={analysis.id}")
        return analysis
    
    def run_single_agent(self, agent_type: str, match_id: int, user_id: int, db: Session) -> Analysis:
        """
        Run a single agent analysis
        
        Args:
            agent_type (str): Type of agent to run ('tournament_info', 'skill_coach', or 'orchestrator')
            match_id (int): ID of the match to analyze
            user_id (int): ID of the user requesting the analysis
            db (Session): Database session
            
        Returns:
            Analysis: The created analysis object
        """
        logger.info(f"Starting {agent_type} analysis for match_id={match_id}")
        
        # Get match data
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            logger.error(f"Match with id {match_id} not found")
            raise ValueError(f"Match with id {match_id} not found")
        
        # Create analysis record
        analysis = Analysis(
            user_id=user_id,
            match_id=match_id,
            title=f"{agent_type.title()} Analysis of {match.player1} vs {match.player2}",
            content=""
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Run the specified agent
        if agent_type == "tournament_info":
            results = self.tournament_info.analyze_match(match_id)
            analysis.tournament_info = results
            analysis.content = f"Tournament Info Analysis for {match.player1} vs {match.player2}"
        
        elif agent_type == "skill_coach":
            results = self.skill_coach.analyze_match(match_id)
            analysis.skill_coach = results
            analysis.content = f"Skill Coach Analysis for {match.player1} vs {match.player2}"
        
        elif agent_type == "orchestrator":
            results = self.orchestrator.analyze_match(match_id)
            analysis.orchestrator = results
            analysis.content = f"Orchestrator Analysis for {match.player1} vs {match.player2}"
            
            # Generate recommendations
            recommendations = self._generate_recommendations(analysis.id, results)
            for rec in recommendations:
                db.add(rec)
        
        else:
            logger.error(f"Unknown agent type: {agent_type}")
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        db.commit()
        db.refresh(analysis)
        
        logger.info(f"{agent_type.title()} analysis completed successfully, id={analysis.id}")
        return analysis
    
    def _generate_recommendations(self, analysis_id: int, orchestrator_data: Dict[str, Any]) -> List[Recommendation]:
        """
        Generate recommendations based on orchestrator output
        
        Args:
            analysis_id (int): ID of the analysis
            orchestrator_data (dict): Orchestrator agent output
            
        Returns:
            List[Recommendation]: List of recommendation objects
        """
        recommendations = []
        
        # Extract improvement areas from orchestrator data
        if "improvement_areas" in orchestrator_data:
            for i, area in enumerate(orchestrator_data["improvement_areas"]):
                # Determine category based on content
                category = "Technical"
                if "tactical" in area.lower() or "position" in area.lower() or "pattern" in area.lower():
                    category = "Tactical"
                elif "mental" in area.lower() or "focus" in area.lower() or "pressure" in area.lower():
                    category = "Mental"
                
                # Create recommendation
                recommendation = Recommendation(
                    analysis_id=analysis_id,
                    title=area,
                    description=f"Improvement area identified: {area}",
                    category=category,
                    priority=i + 1,
                    completed=False
                )
                recommendations.append(recommendation)
        
        return recommendations

# Create a singleton instance
agent_manager = AgentManager()
