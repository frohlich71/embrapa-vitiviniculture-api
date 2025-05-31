from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.auth.dependencies import get_current_active_user, get_current_superuser
from app.auth.models import User
from app.core.config import settings
from app.core.database import get_session
from app.core.pagination import PaginatedResponse
from app.exportation.constants import Category
from app.exportation.crud import (
    clear_exportation,
    count_exportation,
    count_exportation_by_category,
    list_exportation,
    list_exportation_by_category,
)
from app.exportation.ingestor import ExportationIngestor
from app.exportation.models import ExportationRead

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ExportationRead])
def read_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all exportation records with pagination.
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_exportation(session)

    # Get paginated data
    data = list_exportation(session, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.get("/{category}", response_model=PaginatedResponse[ExportationRead])
def read_by_category(
    category: Category,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all exportation records by category with pagination.
    :param category: The category to filter by
    :param session: Database session
    :param page: Page number for pagination
    :param per_page: Items per page
    :return: Paginated list of exportation records
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_exportation_by_category(session, category)

    # Get paginated data
    data = list_exportation_by_category(session, category, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.post("/reingest")
def reingest(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
):
    """
    Endpoint to force re-ingestion of exportation data from source files.
    Requires superuser authentication and ALLOW_REINGEST=true in environment.
    """
    if not settings.ALLOW_REINGEST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reingestion is not allowed in this environment.",
        )
    clear_exportation(session)
    ExportationIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
