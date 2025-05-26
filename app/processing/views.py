from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.processing.constants import Category, Subcategory
from app.processing.crud import (
    clear_processing,
    list_processing,
    list_processing_by_category,
)
from app.processing.ingestor import ProcessingIngestor
from app.processing.models import ProcessingRead

router = APIRouter()

LIMIT = 100
def get_offset(page):
    return (page - 1) * LIMIT


@router.get("/", response_model=list[ProcessingRead])
def read_all(session: Session = Depends(get_session), page: int = 1):
    """
    Endpoint to list all processing records.
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be greater than 0.",
        )

    offset = get_offset(page)
    return list_processing(session, LIMIT, offset)


@router.get("/{category}/{subcategory}", response_model=list[ProcessingRead])
def read_by_path(
    session: Session = Depends(get_session),
    category: Category = None,
    subcategory: Subcategory = None,
    page: int = 1,
):
    """
    Endpoint to list all processing records by the category and subcategory.
    :param session:
    :param category: Category of the processing.
    :param subcategory: Subcategory of the processing.
    :param page: Page number for pagination.
    :return: List of processing records.
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be greater than 0.",
        )

    offset = get_offset(page)
    return list_processing_by_category(session, category, subcategory, LIMIT, offset)


@router.post("/reingest")
def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of processing data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    if not settings.ALLOW_REINGEST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reingestion is not allowed in this environment.",
        )
    clear_processing(session)
    ProcessingIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
