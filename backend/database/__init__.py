from .database import Base, engine, get_db
from .models import User, Tournament, Match, Point, Analysis, Recommendation, UserPreference

# Create all tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)
