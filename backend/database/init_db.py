import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session
from sqlalchemy.orm.session import sessionmaker
from backend.database.database import engine, Base, get_db
from backend.database.models import User, Tournament, Match, Point, Analysis, Recommendation, UserPreference
from backend.app.config import settings
from datetime import datetime

def init_database():
    """Initialize the database with tables and sample data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")
    
    # Get a database session
    db = next(get_db())
    
    # Check if we already have data
    if db.query(Tournament).count() > 0:
        print("Database already contains data. Skipping sample data creation.")
        return
    
    print("Adding sample data...")
    
    # Create sample user
    sample_user = User(
        username="tennis_fan",
        email="tennis_fan@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        is_active=True
    )
    db.add(sample_user)
    db.commit()
    
    # Create user preferences
    user_preferences = UserPreference(
        user_id=sample_user.id,
        skill_level="Intermediate",
        preferred_surface="Hard",
        playing_style="Aggressive Baseliner",
        focus_areas=["Forehand", "Serve", "Mental Game"]
    )
    db.add(user_preferences)
    db.commit()
    
    # Create sample tournaments
    wimbledon = Tournament(
        name="Wimbledon 2025",
        location="London, UK",
        start_date=datetime(2025, 6, 28),
        end_date=datetime(2025, 7, 11),
        surface="Grass",
        category="Grand Slam"
    )
    
    french_open = Tournament(
        name="French Open 2025",
        location="Paris, France",
        start_date=datetime(2025, 5, 26),
        end_date=datetime(2025, 6, 9),
        surface="Clay",
        category="Grand Slam"
    )
    
    db.add(wimbledon)
    db.add(french_open)
    db.commit()
    
    # Create sample matches
    final_match = Match(
        tournament_id=wimbledon.id,
        round="Final",
        player1="Roger Federer",
        player2="Novak Djokovic",
        score="6-4, 7-6, 6-3",
        date=datetime(2025, 7, 11, 14, 0),
        duration=165  # minutes
    )
    
    semifinal_match = Match(
        tournament_id=wimbledon.id,
        round="Semi-final",
        player1="Roger Federer",
        player2="Rafael Nadal",
        score="7-6, 1-6, 6-3, 6-4",
        date=datetime(2025, 7, 9, 14, 0),
        duration=195  # minutes
    )
    
    db.add(final_match)
    db.add(semifinal_match)
    db.commit()
    
    # Create sample points
    point1 = Point(
        match_id=final_match.id,
        point_number=1,
        game_score="0-0",
        point_score="0-0",
        server="Roger Federer",
        winner="Roger Federer",
        first_serve_in=True,
        serve_type="wide",
        rally_length=1,
        winning_shot="ace"
    )
    
    point2 = Point(
        match_id=final_match.id,
        point_number=2,
        game_score="0-0",
        point_score="15-0",
        server="Roger Federer",
        winner="Roger Federer",
        first_serve_in=True,
        serve_type="body",
        return_type="backhand",
        rally_length=5,
        winning_shot="forehand winner"
    )
    
    db.add(point1)
    db.add(point2)
    db.commit()
    
    # Create sample analysis
    analysis = Analysis(
        user_id=sample_user.id,
        match_id=final_match.id,
        title="Federer vs Djokovic Final Analysis",
        content="This is a detailed analysis of the Wimbledon 2025 final match between Roger Federer and Novak Djokovic.",
        tournament_info={
            "key_stats": {
                "aces": {"Federer": 12, "Djokovic": 8},
                "double_faults": {"Federer": 2, "Djokovic": 1},
                "first_serve_percentage": {"Federer": 68, "Djokovic": 72},
                "break_points_converted": {"Federer": "2/5", "Djokovic": "0/3"}
            },
            "match_context": {
                "tournament_stage": "Final",
                "surface_impact": "Fast grass court favoring aggressive play",
                "historical_context": "Their 50th career meeting"
            }
        },
        skill_coach={
            "technical_analysis": {
                "serve": "Excellent wide serves on deuce court",
                "forehand": "Aggressive forehand down the line",
                "backhand": "Slice backhand effectively used to change pace",
                "net_play": "Confident volleys, especially on key points"
            },
            "tactical_analysis": {
                "patterns": "Consistently attacked Djokovic's backhand",
                "court_positioning": "Stayed close to baseline to take time away",
                "shot_selection": "Used drop shots effectively when Djokovic was deep"
            },
            "mental_game": {
                "pressure_points": "Maintained composure on break points",
                "adaptability": "Adjusted tactics after tight second set",
                "focus": "Exceptional concentration throughout the match"
            }
        },
        orchestrator={
            "summary": "Federer dominated with his serve and forehand, taking control of rallies early and preventing Djokovic from finding rhythm.",
            "key_moments": [
                {"game": 5, "set": 1, "description": "Break point conversion with aggressive return"},
                {"game": 12, "set": 2, "description": "Crucial tiebreak mini-break with slice backhand"}
            ],
            "improvement_areas": [
                "Second serve could be more aggressive",
                "More frequent approaches to the net",
                "Backhand return positioning"
            ]
        }
    )
    db.add(analysis)
    db.commit()
    
    # Create sample recommendations
    recommendations = [
        Recommendation(
            analysis_id=analysis.id,
            title="Improve second serve",
            description="Focus on increasing second serve percentage and pace, particularly under pressure.",
            category="Technical",
            priority=1,
            completed=False
        ),
        Recommendation(
            analysis_id=analysis.id,
            title="Net approach frequency",
            description="Increase frequency of approaching the net, especially after wide serves.",
            category="Tactical",
            priority=2,
            completed=False
        ),
        Recommendation(
            analysis_id=analysis.id,
            title="Backhand return positioning",
            description="Stand closer to the baseline when returning second serves to take time away.",
            category="Tactical",
            priority=3,
            completed=True
        )
    ]
    
    for rec in recommendations:
        db.add(rec)
    
    db.commit()
    
    print("Sample data added successfully.")

if __name__ == "__main__":
    init_database()
