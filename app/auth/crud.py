from typing import Optional

from sqlmodel import Session, select

from app.auth.models import User, UserCreate, UserUpdate
from app.auth.utils import get_password_hash, verify_password


def get_user(session: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get user by email"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_users(session: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get list of users"""
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()


def create_user(session: Session, user: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(
    session: Session, user_id: int, user_update: UserUpdate
) -> Optional[User]:
    """Update user"""
    db_user = session.get(User, user_id)
    if not db_user:
        return None

    user_data = user_update.model_dump(exclude_unset=True)
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

    for field, value in user_data.items():
        setattr(db_user, field, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user_id: int) -> bool:
    """Delete user"""
    db_user = session.get(User, user_id)
    if not db_user:
        return False

    session.delete(db_user)
    session.commit()
    return True


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def count_users(session: Session) -> int:
    """Count total number of users"""
    statement = select(User)
    return len(session.exec(statement).all())
