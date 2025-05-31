from typing import Sequence

from sqlmodel import Session, delete, func, select

from app.importation.constants import Category
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


def count_importation_by_category(session: Session, category: Category) -> int:
    """
    Count importation records by category.
    """
    statement = select(func.count(Importation.id)).where(
        Importation.category == category
    )
    result = session.exec(statement)
    return result.one()


def list_importation(
    session: Session, limit: int = None, offset: int = None
) -> Sequence[Importation]:
    """
    Retrieve all importation records from the database.
    """
    statement = select(Importation).order_by(
        Importation.year.desc(), Importation.country
    )

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.execute(statement)
    return result.scalars().all()


def list_importation_by_category(
    session: Session, category: Category, limit: int = None, offset: int = None
) -> Sequence[Importation]:
    """
    Retrieve all importation records from the database by category.
    """
    statement = (
        select(Importation)
        .where(Importation.category == category)
        .order_by(Importation.year.desc(), Importation.country)
    )

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.execute(statement)
    return result.scalars().all()


def get_by_year_and_country_and_category(
    session: Session, year: int, country: str, category: Category
) -> Importation:
    """
    Check if a importation record already exists for the given year, country and category.
    """
    statement = select(Importation).where(
        (Importation.year == year)
        & (Importation.country == country)
        & (Importation.category == category)
    )
    return session.exec(statement).first()


def clear_importation(session: Session) -> None:
    """
    Remove todos os registros da tabela Importation.
    """
    session.exec(delete(Importation))
    session.commit()
