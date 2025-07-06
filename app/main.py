from fastapi import FastAPI
from app.routes import availability, optimize, agencies

app = FastAPI(
    title="Intelligent Hotel Management System",
    description="API FastAPI pour la prédiction de l’occupation et la tarification",
    version="1.0.0"
)

#  Route d'accueil pour éviter l'erreur 404
@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API RMS.AI ",
        "routes_disponibles": [
            "/predict/availability",
            "/predict/optimal",
            "/predict/agency/{agency_id}"
        ],
        "documentation": "/docs"
    }

# Inclusion des routes avec prefix
app.include_router(availability.router, prefix="/predict")
app.include_router(optimize.router, prefix="/predict")
app.include_router(agencies.router, prefix="/predict")
