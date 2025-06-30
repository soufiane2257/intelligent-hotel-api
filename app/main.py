from fastapi import FastAPI
from app.routes import availability, optimize, agencies

app = FastAPI(
    title="Intelligent Hotel Management System",
    description="API FastAPI pour la prédiction de l’occupation et la tarification",
    version="1.0.0"
)

app.include_router(availability.router, prefix="/predict")
app.include_router(optimize.router, prefix="/predict")
app.include_router(agencies.router, prefix="/predict")
