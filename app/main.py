from fastapi import FastAPI
from app.api.v1 import production

app = FastAPI(title="Embrapa Vitiviniculture API")
app.include_router(production.router, prefix="/api/v1/production", tags=["Production"])
