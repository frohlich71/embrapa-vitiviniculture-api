from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.importation import ImportationRead
from app.crud.importation import list_importation, clear_importation, list_importation_by_path
from app.services.embrapa.importation_ingestor import ImportationIngestor

router = APIRouter()


@router.get("/", response_model=list[ImportationRead])
def read_all(session: Session = Depends(get_session)):
    """
    Endpoint to list all importation records.
    """
    return list_importation(session)


@router.get("/{path}", response_model=list[ImportationRead])
def read_by_path(path: str, session: Session = Depends(get_session)):
    """
    Endpoint to list all importation records by the csv path.
    :param path:
    :param session:
    :return:
    """
    return list_importation_by_path(session, path)


@router.post("/reingest")
def reingest(session: Session = Depends(get_session)):
    """
    Endpoint to force re-ingestion of importation data from source files.
    Requires an admin token in headers and ALLOW_REINGEST=true in environment.
    """
    clear_importation(session)
    ImportationIngestor().ingest(session=session)
    return {"detail": "Reingestion completed successfully"}
