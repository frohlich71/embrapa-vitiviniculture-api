from fastapi import FastAPI

from app.commercialization import views as commercialization_views
from app.exportation import views as exportation_views
from app.importation import views as importation_views
from app.processing import views as processing_views
from app.production import views as production_views

app = FastAPI(title="Embrapa Vitiviniculture API")
app.include_router(
    production_views.router, prefix="/api/v1/production", tags=["Production"]
)

app.include_router(
    commercialization_views.router,
    prefix="/api/v1/commercialization",
    tags=["Commercialization"],
)

app.include_router(
    processing_views.router, prefix="/api/v1/processing", tags=["Processing"]
)

app.include_router(
    importation_views.router, prefix="/api/v1/importation", tags=["Importation"]
)

app.include_router(
    exportation_views.router, prefix="/api/v1/exportation", tags=["Exportation"]
)
