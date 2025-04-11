import typer
from sqlmodel import Session

from app.db.session import engine
from app.services.embrapa.production_ingestor import ProductionIngestor
from app.services.embrapa.commercialization_ingestor import CommercializationIngestor

app = typer.Typer()


@app.command()
def run(source: str):
    with Session(engine) as session:
        if source == "production":
            ProductionIngestor().ingest(session)
        elif source == "commercialization":
            CommercializationIngestor().ingest(session)
        else:
            print(f"Unsupported source: {source}")


if __name__ == "__main__":
    app()
