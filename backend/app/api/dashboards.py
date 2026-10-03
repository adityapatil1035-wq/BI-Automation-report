from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.all_models import Dashboard, Dataset
from app.schemas.all_schemas import DashboardOut, DashboardCreate
from app.services.dashboard_generator import generate_dashboard_specs

router = APIRouter(prefix="/dashboards", tags=["Dashboards"])

@router.post("/generate/{dataset_id}", response_model=DashboardOut)
def generate_dashboard_endpoint(dataset_id: int, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    active_path = ds.cleaned_file_path if ds.cleaned_file_path else ds.file_path
    
    specs = generate_dashboard_specs(active_path, domain=ds.domain)
    
    dash = Dashboard(
        title=specs["title"],
        description=f"Automated BI Dashboard generated for dataset '{ds.name}'",
        domain=ds.domain,
        layout_config=specs,
        dataset_id=ds.id,
        workspace_id=1
    )
    
    db.add(dash)
    db.commit()
    db.refresh(dash)
    
    return dash

@router.get("", response_model=List[DashboardOut])
def list_dashboards(db: Session = Depends(get_db)):
    return db.query(Dashboard).order_by(Dashboard.created_at.desc()).all()

@router.get("/{dashboard_id}", response_model=DashboardOut)
def get_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    dash = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if not dash:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return dash
