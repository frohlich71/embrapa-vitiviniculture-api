from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud.commercialization import clear_commercialization, list_commercializations
from app.db.session import get_session
from app.models.commercialization import CommercializationRead
from app.services.embrapa.commercialization_ingestor import CommercializationIngestor
from app.depends import get_current_user # Added
from app.models.user import User # Added

router = APIRouter()


@router.get("/", response_model=list[CommercializationRead])
async def read_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) # Added
):
    """
    Endpoint to list all commercialization records.
    """
    return list_commercializations(session)


@router.post("/reingest")
async def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of commercialization data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    clear_commercialization(session)
    CommercializationIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
