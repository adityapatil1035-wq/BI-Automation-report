from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.all_models import Dataset
from app.schemas.all_schemas import ForecastRequest, ForecastResponse
from app.services.forecaster import generate_time_series_forecast

router = APIRouter(prefix="/forecasting", tags=["Forecasting Studio"])

@router.post("/predict", response_model=ForecastResponse)
def predict_forecast(req: ForecastRequest, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == req.dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    path = ds.cleaned_file_path or ds.file_path
    
    result = generate_time_series_forecast(
        file_path=path,
        date_column=req.date_column,
        value_column=req.value_column,
        horizon_days=req.horizon_days,
        model_type=req.model_type
    )
    
    return result
