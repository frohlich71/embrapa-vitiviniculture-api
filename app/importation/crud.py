from typing import Sequence

from sqlmodel import Session, select, delete, func
from app.importation.models import Importation, ImportationCreate


def create_importation(session: Session, data: ImportationCreate) -> Importation:
    """
    Create a new importation record in the database.
    """
    proc = Importation.model_validate(data)
    session.add(proc)
    session.commit()
    session.refresh(proc)
    return proc


def count_importation(session: Session) -> int:
    """
    Count total importation records in the database.
    """
    statement = select(func.count(Importation.id))
    result = session.exec(statement)
    return result.one()


def count_importation_by_path(session: Session, path: str) -> int:
    """
    Count importation records by path.
    """
    statement = select(func.count(Importation.id)).where(Importation.path == path)
    result = session.exec(statement)
    return result.one()


def list_importation(
    session: Session, limit: int = None, offset: int = None
) -> Sequence[Importation]:
    """
    Retrieve all importation records from the database.
    """
    statement = select(Importation).order_by(Importation.year.desc(), Importation.country)
    
    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)
        
    result = session.execute(statement)
    return result.scalars().all()


def list_importation_by_path(
    session: Session, path: str, limit: int = None, offset: int = None
) -> Sequence[Importation]:
    """
    Retrieve all importation records from the database by path.
    """
    statement = (
        select(Importation)
        .where(Importation.path == path)
        .order_by(Importation.year.desc(), Importation.country)
    )
    
    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)
        
    result = session.execute(statement)
    return result.scalars().all()


def get_by_year_and_country_and_path(
    session: Session, year: int, country: str, path: str
) -> Importation:
    """
    Check if a importation record already exists for the given year and product.
    """
    statement = select(Importation).where(
        (Importation.year == year)
        & (Importation.country == country)
        & (Importation.path == path)
    )
    return session.exec(statement).first()


def clear_importation(session: Session) -> None:
    """
    Remove todos os registros da tabela Importation.
    """
    session.exec(delete(Importation))
    session.commit()
