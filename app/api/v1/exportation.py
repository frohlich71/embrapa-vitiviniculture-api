from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud.exportation import clear_exportation, list_exportation
from app.db.session import get_session
from app.models.exportation import ExportationRead
from app.services.embrapa.exportation_ingestor import ExportationIngestor

router = APIRouter()


@router.get("/", response_model=list[ExportationRead])
async def read_all(session: Session = Depends(get_session)):
    """
    Endpoint to list all export records.
    """
    return list_exportation(session)


@router.post("/reingest")
async def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of export data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    clear_exportation(session)
    ExportationIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}