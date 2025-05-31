from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.auth import crud
from app.auth.dependencies import get_current_active_user, get_current_superuser
from app.auth.models import Token, User, UserCreate, UserRead, UserUpdate
from app.auth.utils import create_access_token
from app.core.config import settings
from app.core.database import get_session
from app.core.pagination import PaginatedResponse

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """Login endpoint to get access token"""
    user = crud.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    """Get current user profile"""
    return current_user


@router.put("/users/me", response_model=UserRead)
async def update_user_me(
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    """Update current user profile"""
    updated_user = crud.update_user(session, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user


@router.get("/users", response_model=PaginatedResponse[UserRead])
async def read_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
    page: int = 1,
    per_page: int = 50,
) -> PaginatedResponse[UserRead]:
    """Get all users (superuser only)"""
    skip = (page - 1) * per_page
    users = crud.get_users(session, skip=skip, limit=per_page)
    total = crud.count_users(session)

    return PaginatedResponse.create(
        data=users, total=total, page=page, per_page=per_page
    )


@router.post("/users", response_model=UserRead)
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
) -> UserRead:
    """Create new user (superuser only)"""
    db_user = crud.get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return crud.create_user(session=session, user=user)


@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
) -> UserRead:
    """Get user by ID (superuser only)"""
    db_user = crud.get_user(session, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
) -> UserRead:
    """Update user (superuser only)"""
    db_user = crud.update_user(session, user_id, user_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
) -> dict:
    """Delete user (superuser only)"""
    if not crud.delete_user(session, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"detail": "User deleted successfully"}
