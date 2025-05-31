from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.auth.dependencies import get_current_active_user, get_current_superuser
from app.auth.models import User
from app.commercialization.crud import (
    clear_commercialization,
    count_commercializations,
    list_commercializations,
)
from app.commercialization.ingestor import CommercializationIngestor
from app.commercialization.models import CommercializationRead
from app.core.config import settings
from app.core.database import get_session
from app.core.pagination import PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CommercializationRead])
async def read_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all commercialization records with pagination.
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_commercializations(session)

    # Get paginated data
    data = list_commercializations(session, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.post("/reingest")
async def reingest(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
):
    """
    Endpoint to force re-ingestion of commercialization data from source files.
    Requires superuser authentication and ALLOW_REINGEST=true in environment.
    """
    if not settings.ALLOW_REINGEST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reingestion is not allowed in this environment.",
        )
    clear_commercialization(session)
    CommercializationIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
