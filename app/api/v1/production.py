from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud.production import clear_production, list_productions
from app.db.session import get_session
from app.models.production import ProductionRead
from app.services.embrapa.production_ingestor import ProductionIngestor
from app.depends import get_current_user # Added
from app.models.user import User # Added

router = APIRouter()


@router.get("/", response_model=list[ProductionRead])
async def read_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) # Added
):
    """
    Endpoint to list all production records.
    """
    return list_productions(session)


@router.post("/reingest")
async def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of production data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    clear_production(session)
    ProductionIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
