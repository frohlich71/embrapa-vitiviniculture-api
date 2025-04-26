from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud.export import clear_exports, list_exports
from app.db.session import get_session
from app.models.export import ExportRead
from app.services.embrapa.export_ingestor import ExportIngestor

router = APIRouter()


@router.get("/", response_model=list[ExportRead])
async def read_all(session: Session = Depends(get_session)):
    """
    Endpoint to list all export records.
    """
    return list_exports(session)


@router.post("/reingest")
async def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of export data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    clear_exports(session)
    ExportIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}