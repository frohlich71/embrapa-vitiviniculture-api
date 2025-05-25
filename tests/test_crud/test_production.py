from app.production.models import ProductionCreate
from app.production.crud import create_production, get_by


def test_create_and_get(db_session):
    data = ProductionCreate(
        year=2022,
        state="RS",
        product="Espumante",
        quantity_liters=12345.6,
        category="OUTROS",
    )
    created = create_production(db_session, data)
    found = get_by(db_session, 2022, "Espumante", "OUTROS")

    assert found is not None
    assert found.id == created.id
