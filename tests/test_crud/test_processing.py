from app.processing.crud import create_processing, get_by_year_and_cultivate_and_path
from app.processing.models import ProcessingCreate


def test_create_and_get(db_session):
    data = ProcessingCreate(
        year=2022, state="RS", cultivate="Tinta", quantity_kg=12345.6, path="ProcessaViniferas"
    )
    created = create_processing(db_session, data)
    found = get_by_year_and_cultivate_and_path(db_session, 2022, "Tinta", "ProcessaViniferas")

    assert found is not None
    assert found.id == created.id
