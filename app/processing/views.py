from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.processing.ingestor import ProcessingIngestor
from app.processing.models import ProcessingRead
from app.processing.crud import (
    list_processing,
    clear_processing,
    list_processing_by_path,
)

router = APIRouter()


@router.get("/", response_model=list[ProcessingRead])
def read_all(session: Session = Depends(get_session)):
    """
    Endpoint to list all processing records.
    """
    return list_processing(session)


@router.get("/{path}", response_model=list[ProcessingRead])
def read_by_path(path: str, session: Session = Depends(get_session)):
    """
    Endpoint to list all processing records by the csv path.
    :param path:
    :param session:
    :return:
    """
    return list_processing_by_path(session, path)


@router.post("/reingest")
def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of processing data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    clear_processing(session)
    ProcessingIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
