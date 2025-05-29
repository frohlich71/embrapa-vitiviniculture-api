from sqlalchemy.orm import Session
from sqlmodel import select # SQLModel uses select

from app.core.security import get_password_hash
from app.models.user import User # Correctly points to the new model
from app.schemas.auth import UserCreate # As specified in the prompt


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Retrieves a user from the database by username.
    """
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    return user


def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
