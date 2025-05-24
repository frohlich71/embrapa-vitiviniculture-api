from fastapi import FastAPI
from app.api.v1 import production, commercialization, processing, importation, exportation, debug

app = FastAPI(title="Embrapa Vitiviniculture API")
app.include_router(production.router,
                   prefix="/api/v1/production", tags=["Production"])

app.include_router(commercialization.router,
                   prefix="/api/v1/commercialization", tags=["Commercialization"])

app.include_router(processing.router,
                   prefix="/api/v1/processing", tags=["Processing"])

app.include_router(importation.router,
                   prefix="/api/v1/importation", tags=["Importation"])

app.include_router(exportation.router,
                   prefix="/api/v1/exportation", tags=["Exportation"])

app.include_router(debug.router, prefix="/api/v1/debug", tags=["Debug"])
