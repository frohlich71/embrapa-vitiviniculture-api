from typing import Sequence

from sqlmodel import Session, delete, select

from app.models.production import Production, ProductionCreate


def create_production(session: Session, data: ProductionCreate) -> Production:
    """
    Create a new production record in the database.
    """
    prod = Production.model_validate(data)
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return prod


def list_productions(session: Session) -> Sequence[Production]:
    """
    Retrieve all production records from the database.
    """
    statement = select(Production)
    result = session.execute(statement)
    return result.scalars().all()

def get_by_year_and_product(
    session: Session, year: int, product: str
) -> Production:
    """
    Check if a production record already exists for the given year and product.
    """
    statement = select(Production).where(
        (Production.year == year) & (Production.product == product)
    )
    return session.exec(statement).first()


def clear_production(session: Session) -> None:
    """
    Remove todos os registros da tabela production.
    """
    session.exec(delete(Production))
    session.commit()
