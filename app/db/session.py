from sqlmodel import create_engine, Session
from app.core.config import settings

# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

def get_session():
    """
    Dependency function to yield a SQLModel session for database access.
    """
    with Session(engine) as session:
        yield session
