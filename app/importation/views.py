from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session

from app.core.config import settings
from app.core.pagination import PaginatedResponse
from app.core.database import get_session
from app.importation.models import ImportationRead
from app.importation.crud import (
    count_importation,
    count_importation_by_path,
    list_importation,
    clear_importation,
    list_importation_by_path,
)
from app.importation.ingestor import ImportationIngestor

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ImportationRead])
def read_all(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page")
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
        data=data,
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/{path}", response_model=PaginatedResponse[ImportationRead])
def read_by_path(
    path: str, 
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page")
):
    """
    Endpoint to list all importation records by the csv path with pagination.
    :param path: The CSV path to filter by
    :param session: Database session
    :param page: Page number for pagination
    :param per_page: Items per page
    :return: Paginated list of importation records
    """
    offset = (page - 1) * per_page
    
    # Get total count
    total = count_importation_by_path(session, path)
    
    # Get paginated data
    data = list_importation_by_path(session, path, per_page, offset)
    
    return PaginatedResponse.create(
        data=data,
        total=total,
        page=page,
        per_page=per_page
    )


@router.post("/reingest")
def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of importation data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    if not settings.ALLOW_REINGEST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reingestion is not allowed in this environment.",
        )
    clear_importation(session)
    ImportationIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
