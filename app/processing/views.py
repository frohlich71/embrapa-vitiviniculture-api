from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.auth.dependencies import get_current_active_user, get_current_superuser
from app.auth.models import User
from app.core.config import settings
from app.core.database import get_session
from app.core.pagination import PaginatedResponse
from app.processing.constants import Category, Subcategory
from app.processing.crud import (
    clear_processing,
    count_processing,
    count_processing_by_category,
    list_processing,
    list_processing_by_category,
)
from app.processing.ingestor import ProcessingIngestor
from app.processing.models import ProcessingRead

router = APIRouter()

LIMIT = 100


def get_offset(page):
    return (page - 1) * LIMIT


@router.get("/", response_model=PaginatedResponse[ProcessingRead])
def read_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all processing records with pagination.
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_processing(session)

    # Get paginated data
    data = list_processing(session, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.get("/{category}", response_model=PaginatedResponse[ProcessingRead])
@router.get(
    "/{category}/{subcategory}", response_model=PaginatedResponse[ProcessingRead]
)
def read_by_path(
    category: Category,
    subcategory: Subcategory | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all processing records by the category and subcategory with pagination.
    :param category: Category of the processing.
    :param subcategory: Subcategory of the processing (optional).
    :param session: Database session.
    :param page: Page number for pagination.
    :param per_page: Items per page.
    :return: Paginated list of processing records.
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_processing_by_category(session, category, subcategory)

    # Get paginated data
    data = list_processing_by_category(session, category, subcategory, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.post("/reingest")
def reingest(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
):
    """
    Endpoint to force re-ingestion of processing data from source files.
    Requires superuser authentication and ALLOW_REINGEST=true in environment.
    """
    if not settings.ALLOW_REINGEST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reingestion is not allowed in this environment.",
        )
    clear_processing(session)
    ProcessingIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
