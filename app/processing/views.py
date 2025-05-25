from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.processing.crud import (
    clear_processing,
    list_processing,
    list_processing_by_path,
)
from app.processing.ingestor import ProcessingIngestor
from app.processing.models import ProcessingRead

router = APIRouter()


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

    limit = 100
    offset = (page - 1) * limit
    return list_processing(session, limit, offset)


@router.get("/{category}/{subcategory}", response_model=list[ProcessingRead])
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
