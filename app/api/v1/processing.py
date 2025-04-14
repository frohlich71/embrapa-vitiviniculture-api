from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.processing import ProcessingRead
from app.crud.processing import list_processing, clear_processing
from app.services.embrapa.processing_ingestor import ProcessingIngestor

router = APIRouter()

@router.get("/", response_model=list[ProcessingRead])
def read_all(session: Session = Depends(get_session)):
  """
  Endpoint to list all production records.
  """
  return list_processing(session)



@router.post("/reingest")
def reingest(session: Session = Depends(get_session)):
  """
  Endpoint to force re-ingestion of processing data from source files.
  Requires an admin token in headers and ALLOW_REINGEST=true in environment.
  """
  clear_processing(session)
  ProcessingIngestor().ingest(session=session)
  return {"detail": "Reingestion completed successfully"}