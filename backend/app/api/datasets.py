import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.config import settings
from app.models.all_models import Dataset, User
from app.schemas.all_schemas import DatasetOut, CleanDatasetRequest
from app.services.data_ingestion import analyze_dataset_structure
from app.services.data_cleaning import clean_dataset
from app.services.domain_detector import detect_business_domain
from app.services.data_ingestion import load_dataframe

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("/upload", response_model=DatasetOut)
def upload_dataset(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".csv", ".xlsx", ".xls", ".json"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Supported: CSV, XLSX, XLS, JSON")
        
    save_name = f"{os.path.splitext(file.filename)[0]}_{os.urandom(4).hex()}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, save_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Analyze dataset structure
    try:
        profile = analyze_dataset_structure(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse data file: {str(e)}")

    # Detect domain
    try:
        df = load_dataframe(file_path)
        detected_domain, confidence, _ = detect_business_domain(df)
    except Exception:
        detected_domain = "Sales"

    dataset_obj = Dataset(
        name=name or file.filename,
        filename=file.filename,
        file_path=file_path,
        file_type=ext.replace(".", ""),
        row_count=profile["row_count"],
        col_count=profile["col_count"],
        data_quality_score=profile["data_quality_score"],
        domain=detected_domain,
        quality_summary=profile["quality_summary"],
        column_metadata=profile["column_metadata"],
        workspace_id=1
    )
    
    db.add(dataset_obj)
    db.commit()
    db.refresh(dataset_obj)
    
    return dataset_obj

@router.get("", response_model=List[DatasetOut])
def list_datasets(db: Session = Depends(get_db)):
    return db.query(Dataset).order_by(Dataset.created_at.desc()).all()

@router.get("/{dataset_id}", response_model=DatasetOut)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return ds

@router.post("/{dataset_id}/clean", response_model=DatasetOut)
def clean_dataset_endpoint(
    dataset_id: int,
    req: CleanDatasetRequest,
    db: Session = Depends(get_db)
):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    base_name = os.path.splitext(os.path.basename(ds.file_path))[0]
    cleaned_filename = f"cleaned_{base_name}.csv"
    cleaned_path = os.path.join(settings.UPLOAD_DIR, cleaned_filename)
    
    out_path, log, summary = clean_dataset(
        file_path=ds.file_path,
        output_cleaned_path=cleaned_path,
        impute_missing=req.impute_missing,
        remove_duplicates=req.remove_duplicates,
        handle_outliers=req.handle_outliers,
        date_parsing=req.date_parsing
    )
    
    ds.cleaned_file_path = out_path
    ds.transformation_log = log
    ds.data_quality_score = summary["cleaned_quality_score"]
    
    db.commit()
    db.refresh(ds)
    return ds

@router.put("/{dataset_id}/domain", response_model=DatasetOut)
def set_dataset_domain(dataset_id: int, domain: str, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    ds.domain = domain
    db.commit()
    db.refresh(ds)
    return ds
