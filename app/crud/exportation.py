from typing import Sequence

from sqlmodel import Session, select, delete
from app.models.exportation import Exportation, ExportationCreate


def create_exportation(session: Session, data: ExportationCreate) -> Exportation:
    """
    Create a new importation record in the database.
    """
    proc = Exportation.model_validate(data)
    session.add(proc)
    session.commit()
    session.refresh(proc)
    return proc


def list_exportation(session: Session) -> Sequence[Exportation]:
    """
    Retrieve all importation records from the database.
    """
    return session.exec(select(Exportation)).all()


def list_exportation_by_path(session: Session, path: str) -> Sequence[Exportation]:
    """
    Retrieve all importation records from the database by path.
    """
    return session.exec(select(Exportation).where(Exportation.path == path)).all()


def get_by_year_and_country_and_path(
    session: Session, year: int, country: str, path: str
) -> Exportation:
    """
    Check if a importation record already exists for the given year and product.
    """
    statement = select(Exportation).where(
        (Exportation.year == year)
        & (Exportation.country == country)
        & (Exportation.path == path)
    )
    return session.exec(statement).first()


def clear_exportation(session: Session) -> None:
    """
    Remove todos os registros da tabela Importation.
    """
    session.exec(delete(Exportation))
    session.commit()
