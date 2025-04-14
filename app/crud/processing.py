from typing import Sequence

from sqlmodel import Session, select, delete
from app.models.processing import Processing, ProcessingCreate


def create_processing(session: Session, data: ProcessingCreate) -> Processing:
    """
    Create a new prcessing record in the database.
    """
    proc = Processing.model_validate(data)
    session.add(proc)
    session.commit()
    session.refresh(proc)
    return proc


def list_processing(session: Session) -> Sequence[Processing]:
    """
    Retrieve all processing records from the database.
    """
    return session.exec(select(Processing)).all()


def get_by_year_and_cultivate(session: Session, year: int, cultivate: str) -> Processing:
    """
    Check if a processing record already exists for the given year and product.
    """
    statement = select(Processing).where(
        (Processing.year == year) & (Processing.cultivate == cultivate)
    )
    return session.exec(statement).first()


def clear_processing(session: Session) -> None:
    """
    Remove todos os registros da tabela processing.
    """
    session.exec(delete(Processing))
    session.commit()
