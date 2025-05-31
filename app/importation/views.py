from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.auth.dependencies import get_current_superuser
from app.auth.models import User
from app.core.config import settings
from app.core.database import get_session
from app.core.pagination import PaginatedResponse
from app.importation.constants import Category
from app.importation.crud import (
    clear_importation,
    count_importation,
    count_importation_by_category,
    list_importation,
    list_importation_by_category,
)
from app.importation.ingestor import ImportationIngestor
from app.importation.models import ImportationRead

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ImportationRead])
def read_all(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all importation records with pagination.
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_importation(session)

    # Get paginated data
    data = list_importation(session, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.get("/{category}", response_model=PaginatedResponse[ImportationRead])
def read_by_category(
    category: Category,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all importation records by category with pagination.
    :param category: The category to filter by
    :param session: Database session
    :param page: Page number for pagination
    :param per_page: Items per page
    :return: Paginated list of importation records
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_importation_by_category(session, category)

    # Get paginated data
    data = list_importation_by_category(session, category, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.post("/reingest")
def reingest(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
):
    """
    Endpoint to force re-ingestion of importation data from source files.
    Requires superuser authentication and ALLOW_REINGEST=true in environment.
    """
    if not settings.ALLOW_REINGEST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reingestion is not allowed in this environment.",
        )
    clear_importation(session)
    ImportationIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
