from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

router = APIRouter()
model = joblib.load("app/models/model_occupancy_pricing_optimizer.pkl")

class OptimizeRequest(BaseModel):
    date_str: str
    iseventday: int
    vacance_MA: int
    roomType: int
    total_available: int

@router.post("/optimal")
def recommend(request: OptimizeRequest):
    date_obj = pd.to_datetime(request.date_str)
    day, month, weekday = date_obj.day, date_obj.month, date_obj.weekday()

    best_taux = 0.01
    best_total_price = -np.inf

    for taux in np.linspace(1, 100, 100):
        input_data = pd.DataFrame([{
            "day": day,
            "month": month,
            "weekday": weekday,
            "roomType": request.roomType,
            "occupancy": taux,
            "iseventday": request.iseventday,
            "vacance_MA": request.vacance_MA,
            "total_available": request.total_available
        }])
        price = model.predict(input_data)[0]
        if price > best_total_price:
            best_total_price = price
            best_taux = taux

    chambres_occupees = (best_taux * request.total_available) / 100
    mean_price = best_total_price / chambres_occupees if chambres_occupees > 0 else 0.0

    return {
        "optimal_occupancy": round(best_taux, 2),
        "max_total_price": round(best_total_price, 2),
        "mean_price_per_room": round(mean_price, 2)
    }
