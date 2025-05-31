from typing import Sequence

from sqlmodel import Session, delete, func, select

from app.exportation.models import Exportation, ExportationCreate
from app.exportation.constants import Category


def create_exportation(session: Session, data: ExportationCreate) -> Exportation:
    """
    Create a new exportation record in the database.
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


def count_exportation_by_category(session: Session, category: Category) -> int:
    """
    Count exportation records by category.
    """
    statement = select(func.count(Exportation.id)).where(
        Exportation.category == category
    )
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


def list_exportation_by_category(
    session: Session, category: Category, limit: int = None, offset: int = None
) -> Sequence[Exportation]:
    """
    Retrieve all exportation records from the database by category.
    """
    statement = (
        select(Exportation)
        .where(Exportation.category == category)
        .order_by(Exportation.year.desc(), Exportation.country)
    )

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.exec(statement)
    return result.all()


def get_by_year_and_country_and_category(
    session: Session, year: int, country: str, category: Category
) -> Exportation:
    """
    Check if a exportation record already exists for the given year, country and category.
    """
    statement = select(Exportation).where(
        (Exportation.year == year)
        & (Exportation.country == country)
        & (Exportation.category == category)
    )
    return session.exec(statement).first()


def clear_exportation(session: Session) -> None:
    """
    Remove todos os registros da tabela Exportation.
    """
    session.exec(delete(Exportation))
    session.commit()
