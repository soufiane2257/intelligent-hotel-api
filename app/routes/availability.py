from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib

router = APIRouter()
model = joblib.load("app/models/model_total_available_rooms.pkl")

class AvailabilityRequest(BaseModel):
    date_str: str
    iseventday: int
    vacance_MA: int
    roomType: int

@router.post("/availability")
def predict_total_available(request: AvailabilityRequest):
    date_obj = pd.to_datetime(request.date_str)
    input_data = pd.DataFrame([{
        "day": date_obj.day,
        "month": date_obj.month,
        "weekday": date_obj.weekday(),
        "roomType": request.roomType,
        "iseventday": request.iseventday,
        "vacance_MA": request.vacance_MA
    }])
    prediction = model.predict(input_data)
    return {"total_available_predicted": round(prediction[0])}
