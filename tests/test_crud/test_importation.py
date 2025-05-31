from app.importation.crud import create_importation, get_by_year_and_country_and_path
from app.importation.models import ImportationCreate


def test_create_and_get(db_session):
    data = ImportationCreate(
        year=2022,
        state="RS",
        country="Alemanha",
        quantity_kg=12345.6,
        value_us=92.500,
        path="ImpVinhos",
    )
    created = create_importation(db_session, data)
    found = get_by_year_and_country_and_path(db_session, 2022, "Alemanha", "ImpVinhos")

    assert found is not None
    assert found.id == created.id
