from app.models.production import ProductionCreate
from app.crud.production import create_production, get_by_year_and_product


def test_create_and_get(db_session):
    data = ProductionCreate(
        year=2022, state="RS", product="Espumante", quantity_liters=12345.6
    )
    created = create_production(db_session, data)
    found = get_by_year_and_product(db_session, 2022, "Espumante")

    assert found is not None
    assert found.id == created.id
