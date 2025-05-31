from typing import Sequence

from sqlmodel import Session, delete, select, func

from app.production.constants import Category
from app.production.models import Production, ProductionCreate


def create_production(session: Session, data: ProductionCreate) -> Production:
    """
    Create a new production record in the database.
    """
    prod = Production.model_validate(data)
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return prod


def list_productions(
    session: Session, limit: int = None, offset: int = None
) -> Sequence[Production]:
    """
    Retrieve all production records from the database.
    """
    statement = select(Production).order_by(Production.year.desc(), Production.product)

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.exec(statement)
    return result.all()


def list_productions_by_category(
    session: Session, category: Category, limit: int = None, offset: int = None
) -> Sequence[Production]:
    """
    Retrieve all production records from the database.
    """
    statement = (
        select(Production)
        .where(Production.category == category)
        .order_by(Production.year.desc(), Production.product)
    )

    if offset:
        statement = statement.offset(offset)
    if limit:
        statement = statement.limit(limit)

    result = session.exec(statement)
    return result.all()


def get_by(session: Session, year: int, product: str, category: str) -> Production:
    """
    Check if a production record already exists for the given year and product.
    """
    statement = select(Production).where(
        (Production.year == year)
        & (Production.product == product)
        & (Production.category == category)
    )
    return session.exec(statement).first()


def clear_production(session: Session) -> None:
    """
    Clear all production records from the database.
    """
    statement = delete(Production)
    session.exec(statement)
    session.commit()


def count_productions(session: Session) -> int:
    """
    Count total production records in the database.
    """
    statement = select(func.count(Production.id))
    result = session.exec(statement)
    return result.one()


def count_productions_by_category(session: Session, category: Category) -> int:
    """
    Count production records by category.
    """
    statement = select(func.count(Production.id)).where(Production.category == category)
    result = session.exec(statement)
    return result.one()
