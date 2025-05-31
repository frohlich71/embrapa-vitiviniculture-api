from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session

from app.auth.dependencies import get_current_superuser
from app.auth.models import User
from app.core.config import settings
from app.core.pagination import PaginatedResponse
from app.core.database import get_session
from app.exportation.crud import (
    clear_exportation,
    count_exportation,
    count_exportation_by_path,
    list_exportation,
    list_exportation_by_path,
)
from app.exportation.models import ExportationRead
from app.exportation.ingestor import ExportationIngestor

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ExportationRead])
async def read_all(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all export records with pagination.
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_exportation(session)

    # Get paginated data
    data = list_exportation(session, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.get("/{path}", response_model=PaginatedResponse[ExportationRead])
async def read_by_path(
    path: str,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page"),
):
    """
    Endpoint to list all exportation records by the csv path with pagination.
    :param path: The CSV path to filter by
    :param session: Database session
    :param page: Page number for pagination
    :param per_page: Items per page
    :return: Paginated list of exportation records
    """
    offset = (page - 1) * per_page

    # Get total count
    total = count_exportation_by_path(session, path)

    # Get paginated data
    data = list_exportation_by_path(session, path, per_page, offset)

    return PaginatedResponse.create(
        data=data, total=total, page=page, per_page=per_page
    )


@router.post("/reingest")
async def reingest(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_superuser),
):
    """
    Endpoint to force re-ingestion of export data from source files.
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
