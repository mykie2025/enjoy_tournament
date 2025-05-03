from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    analyses = relationship("Analysis", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user")

class Tournament(Base):
    __tablename__ = "tournaments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    surface = Column(String)
    category = Column(String)  # Grand Slam, ATP 1000, etc.
    external_id = Column(String, nullable=True, index=True)  # ID from external API
    is_selected = Column(Boolean, default=False)  # Track if tournament is selected
    status = Column(String, default="upcoming")  # upcoming, live, ended
    
    # Relationships
    matches = relationship("Match", back_populates="tournament")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    round = Column(String)  # Final, Semi-final, etc.
    player1 = Column(String)
    player2 = Column(String)
    score = Column(String)
    date = Column(DateTime)
    duration = Column(Integer)  # in minutes
    
    # Relationships
    tournament = relationship("Tournament", back_populates="matches")
    analyses = relationship("Analysis", back_populates="match")
    points = relationship("Point", back_populates="match")

class Point(Base):
    __tablename__ = "points"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    point_number = Column(Integer)
    game_score = Column(String)
    point_score = Column(String)
    server = Column(String)
    winner = Column(String)
    first_serve_in = Column(Boolean, nullable=True)
    serve_type = Column(String, nullable=True)
    return_type = Column(String, nullable=True)
    rally_length = Column(Integer, nullable=True)
    winning_shot = Column(String, nullable=True)
    
    # Relationships
    match = relationship("Match", back_populates="points")

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    match_id = Column(Integer, ForeignKey("matches.id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    content = Column(Text)
    
    # JSON fields for agent outputs
    tournament_info = Column(JSON, nullable=True)
    skill_coach = Column(JSON, nullable=True)
    orchestrator = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    match = relationship("Match", back_populates="analyses")
    recommendations = relationship("Recommendation", back_populates="analysis")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    title = Column(String)
    description = Column(Text)
    category = Column(String)  # Technical, Tactical, Mental, etc.
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="recommendations")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_level = Column(String)
    preferred_surface = Column(String)
    playing_style = Column(String)
    focus_areas = Column(JSON)  # Array of focus areas
    
    # Relationships
    user = relationship("User", back_populates="preferences")
