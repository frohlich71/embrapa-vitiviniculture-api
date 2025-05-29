from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.processing import ProcessingRead
from app.crud.processing import list_processing, clear_processing, list_processing_by_path
from app.services.embrapa.processing_ingestor import ProcessingIngestor
from app.depends import get_current_user # Added
from app.models.user import User # Added

router = APIRouter()

@router.get("/", response_model=list[ProcessingRead])
def read_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) # Added
):
  """
  Endpoint to list all processing records.
  """
  return list_processing(session)


@router.get("/{path}", response_model=list[ProcessingRead])
def read_by_path(
    path: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) # Added
):
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