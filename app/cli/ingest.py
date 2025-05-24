import typer
from sqlmodel import Session

from app.db.session import engine
from app.services.embrapa.processing_ingestor import ProcessingIngestor
from app.services.embrapa.production_ingestor import ProductionIngestor
from app.services.embrapa.commercialization_ingestor import CommercializationIngestor
from app.services.embrapa.importation_ingestor import ImportationIngestor
from app.services.embrapa.exportation_ingestor import ExportationIngestor

app = typer.Typer()


@app.command()
def run(source: str):
    with Session(engine) as session:
        if source == "production":
            ProductionIngestor().ingest(session)
        elif source == "commercialization":
            CommercializationIngestor().ingest(session)
        elif source == "processing":
            ProcessingIngestor().ingest(session)
        elif source == "importation":
            ImportationIngestor().ingest(session)
        elif source == "exportation":
            ExportationIngestor().ingest(session)
        else:
            print("Unsupported source: {source}")


if __name__ == "__main__":
    app()
