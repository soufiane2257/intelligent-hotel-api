from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os

router = APIRouter()

class AgencyRequest(BaseModel):
    date_str: str
    iseventday: int
    vacance_MA: int
    roomType: int

@router.post("/agency/{agency_id}")
def predict_agency(agency_id: str, request: AgencyRequest):
    model_path = f"app/models/agencies/agency_{agency_id}.pkl"

    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Agency model not found")

    model = joblib.load(model_path)

    date_obj = pd.to_datetime(request.date_str)
    input_data = pd.DataFrame([{
        'day': date_obj.day,
        'month': date_obj.month,
        'weekday': date_obj.weekday(),
        'roomType': request.roomType,
        'iseventday': request.iseventday,
        'vacance_MA': request.vacance_MA
    }])

    y_pred = model.predict(input_data)[0]
    return {
        "booked": int(round(y_pred[0])),
        "available": int(round(y_pred[1]))
    }
