import typer
from sqlmodel import Session

from app.auth.init_admin import create_admin_user
from app.core.database import engine
from app.processing.ingestor import ProcessingIngestor
from app.production.ingestor import ProductionIngestor
from app.commercialization.ingestor import CommercializationIngestor
from app.exportation.ingestor import ExportationIngestor
from app.importation.ingestor import ImportationIngestor

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


@app.command()
def init_admin():
    """Initialize admin user"""
    create_admin_user()


if __name__ == "__main__":
    app()
