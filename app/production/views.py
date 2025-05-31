from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.auth.dependencies import get_current_active_user, get_current_superuser
from app.auth.models import User
from app.core.config import settings
from app.core.database import get_session
from app.core.pagination import PaginatedResponse
from app.production.constants import Category
from app.production.crud import (
    clear_production,
    count_productions,
    count_productions_by_category,
    list_productions,
    list_productions_by_category,
)
from app.production.ingestor import ProductionIngestor
from app.production.models import ProductionRead

router = APIRouter()

LIMIT = 100


def get_offset(page):
    return (page - 1) * LIMIT


@router.get("/", response_model=PaginatedResponse[ProductionRead])
async def read_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all production records with pagination.
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_productions(session)

    # Get paginated data
    data = list_productions(session, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.get("/{category}", response_model=PaginatedResponse[ProductionRead])
async def read_by_category(
    category: Category,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all production records by category with pagination.
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_productions_by_category(session, category)

    # Get paginated data
    data = list_productions_by_category(session, category, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.post("/reingest")
async def reingest(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
):
    """
    Endpoint to force re-ingestion of production data from source files.
    Requires superuser authentication and ALLOW_REINGEST=true in environment.
    """
    if not settings.ALLOW_REINGEST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reingestion is not allowed in this environment.",
        )

    clear_production(session)
    ProductionIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
