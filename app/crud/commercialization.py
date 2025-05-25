from __future__ import annotations

from typing import Sequence

from sqlmodel import Session, delete, select

from app.models.commercialization import Commercialization, CommercializationCreate


def create_commercialization(
    session: Session, data: CommercializationCreate
) -> Commercialization:
    """
    Create a new commercialization record in the database.
    """
    prod = Commercialization.model_validate(data)
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return prod


def list_commercializations(session: Session) -> Sequence[Commercialization]:
    """
    Retrieve all commercialization records from the database.
    """
    statement = select(Commercialization)
    result = session.execute(statement)
    return result.scalars().all()


def get_by_year_and_product(
    session: Session, year: int, product: str
) -> Commercialization | None:
    """
    Check if a commercialization record already exists for the given year and product.
    """
    statement = select(Commercialization).where(
        (Commercialization.year == year) & (Commercialization.product == product)
    )
    return session.exec(statement).first()


def clear_commercialization(session: Session) -> None:
    """
    Remove todos os registros da tabela commercialization.
    """
    session.exec(delete(Commercialization))
    session.commit()
