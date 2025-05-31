from typing import Sequence

from sqlmodel import Session, select, delete, func
from app.exportation.models import Exportation, ExportationCreate


def create_exportation(session: Session, data: ExportationCreate) -> Exportation:
    """
    Create a new importation record in the database.
    """
    proc = Exportation.model_validate(data)
    session.add(proc)
    session.commit()
    session.refresh(proc)
    return proc


def count_exportation(session: Session) -> int:
    """
    Count total exportation records in the database.
    """
    statement = select(func.count(Exportation.id))
    result = session.exec(statement)
    return result.one()


def count_exportation_by_path(session: Session, path: str) -> int:
    """
    Count exportation records by path.
    """
    statement = select(func.count(Exportation.id)).where(Exportation.path == path)
    result = session.exec(statement)
    return result.one()


def list_exportation(
    session: Session, limit: int = None, offset: int = None
) -> Sequence[Exportation]:
    """
    Retrieve all exportation records from the database.
    """
    statement = select(Exportation).order_by(
        Exportation.year.desc(), Exportation.country
    )

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.exec(statement)
    return result.all()


def list_exportation_by_path(
    session: Session, path: str, limit: int = None, offset: int = None
) -> Sequence[Exportation]:
    """
    Retrieve all exportation records from the database by path.
    """
    statement = (
        select(Exportation)
        .where(Exportation.path == path)
        .order_by(Exportation.year.desc(), Exportation.country)
    )

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.exec(statement)
    return result.all()


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
