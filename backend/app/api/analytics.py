from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.core.database import get_db
from app.models.all_models import Dataset
from app.services.kpi_engine import compute_dataset_kpis
from app.services.insight_engine import generate_ai_business_insights
from app.services.anomaly_detector import detect_anomalies_in_dataset

router = APIRouter(prefix="/analytics", tags=["Analytics & AI Insights"])

@router.get("/{dataset_id}/kpis")
def get_kpis(dataset_id: int, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    path = ds.cleaned_file_path or ds.file_path
    return compute_dataset_kpis(path, domain=ds.domain)

@router.get("/{dataset_id}/insights")
def get_insights(dataset_id: int, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    path = ds.cleaned_file_path or ds.file_path
    return generate_ai_business_insights(path, domain=ds.domain)

@router.get("/{dataset_id}/anomalies")
def get_anomalies(dataset_id: int, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    path = ds.cleaned_file_path or ds.file_path
    return detect_anomalies_in_dataset(path)
