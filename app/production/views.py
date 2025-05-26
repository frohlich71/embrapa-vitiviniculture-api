from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.production.constants import Category
from app.production.crud import (
    clear_production,
    list_productions,
    list_productions_by_category,
)
from app.production.ingestor import ProductionIngestor
from app.production.models import ProductionRead

router = APIRouter()

LIMIT = 100
def get_offset(page):
    return (page - 1) * LIMIT


@router.get("/", response_model=list[ProductionRead])
async def read_all(session: Session = Depends(get_session), page: int = 1):
    """
    Endpoint to list all production records.
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be greater than 0.",
        )

    offset = get_offset(page)
    return list_productions(session, LIMIT, offset)


@router.get("/{category}", response_model=list[ProductionRead])
async def read_by_category(
    session: Session = Depends(get_session), category: Category = None, page: int = 1
):
    """
    Endpoint to list all production records.
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be greater than 0.",
        )

    offset = get_offset(page)
    return list_productions_by_category(session, category, LIMIT, offset)


@router.post("/reingest")
async def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of production data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    if not settings.ALLOW_REINGEST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reingestion is not allowed in this environment.",
        )

    clear_production(session)
    ProductionIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
