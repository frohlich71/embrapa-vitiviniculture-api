from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError # Already handled in verify_token but good to be aware

from app.core.security import verify_token
from app.crud.user import get_user_by_username
from app.db.session import get_session # Assuming this provides a DB session
from app.models.user import User # To type hint the return value
from app.schemas.auth import TokenData # To handle the data from token payload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
) -> User:
    username = verify_token(token=token, credentials_exception=credentials_exception)
    if username is None: # verify_token should raise, but as a safeguard
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception # User not found in DB
    return user
