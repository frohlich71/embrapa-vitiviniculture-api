from typing import Sequence

from sqlmodel import Session, delete, select, func

from app.processing.constants import Category, Subcategory
from app.processing.models import Processing, ProcessingCreate


def _default_order_by():
    """
    Default order by clause for processing records.
    """
    return (
        Processing.year.desc(),
        Processing.category,
        Processing.subcategory,
        Processing.cultivate,
    )


def create_processing(session: Session, data: ProcessingCreate) -> Processing:
    """
    Create a new prcessing record in the database.
    """
    proc = Processing.model_validate(data)
    session.add(proc)
    session.commit()
    session.refresh(proc)
    return proc


def list_processing(
    session: Session, limit: int = None, offset: int = None
) -> Sequence[Processing]:
    """
    Retrieve all processing records from the database.
    """
    statement = select(Processing).order_by(*_default_order_by())

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.exec(statement)
    return result.all()


def list_processing_by_category(
    session: Session,
    category: Category,
    subcategory: Subcategory = None,
    limit: int = None,
    offset: int = None,
) -> Sequence[Processing]:
    """
    Retrieve all processing records from the database by path.
    """
    statement = select(Processing).where(Processing.category == category)
    if subcategory:
        statement = statement.where(Processing.subcategory == subcategory)

    statement = statement.order_by(*_default_order_by())

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.exec(statement)
    return result.all()


def get_by_year_and_cultivate_and_category(
    session: Session,
    year: int,
    cultivate: str,
    category: str,
    subcategory: str,
) -> Processing | None:
    statement = select(Processing).where(
        (Processing.year == year)
        & (Processing.cultivate == cultivate)
        & (Processing.category == category)
        & (Processing.subcategory == subcategory)
    )
    return session.exec(statement).first()


def clear_processing(session: Session) -> None:
    """
    Remove todos os registros da tabela processing.
    """
    session.exec(delete(Processing))
    session.commit()


def count_processing(session: Session) -> int:
    """
    Count total processing records in the database.
    """
    statement = select(func.count(Processing.id))
    result = session.exec(statement)
    return result.one()


def count_processing_by_category(
    session: Session,
    category: Category,
    subcategory: Subcategory = None,
) -> int:
    """
    Count processing records by category and subcategory.
    """
    statement = select(func.count(Processing.id)).where(Processing.category == category)
    if subcategory:
        statement = statement.where(Processing.subcategory == subcategory)

    result = session.exec(statement)
    return result.one()
