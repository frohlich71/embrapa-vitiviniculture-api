from fastapi import FastAPI
from app.api.v1 import production, commercialization

app = FastAPI(title="Embrapa Vitiviniculture API")

app.include_router(production.router, prefix="/api/v1/production", tags=["Production"])

app.include_router(commercialization.router, prefix="/api/v1/commercialization", tags=["Commercialization"])
