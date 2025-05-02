import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tennis_tournament.db")
    
    # OpenAI API Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    # Agent Model Settings
    ORCHESTRATOR_MODEL: str = os.getenv("ORCHESTRATOR_MODEL", "gpt-4o")
    TOURNAMENT_INFO_MODEL: str = os.getenv("TOURNAMENT_INFO_MODEL", "gpt-4o-mini")
    TENNIS_SKILL_COACH_MODEL: str = os.getenv("TENNIS_SKILL_COACH_MODEL", "gpt-4o-mini")
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()
