import os
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.all_models import Dataset, Dashboard
from app.services.pdf_report_generator import generate_pdf_report
from app.services.excel_report_generator import generate_excel_report

router = APIRouter(prefix="/reports", tags=["Report Generation"])

@router.post("/generate-pdf/{dataset_id}")
def generate_pdf_endpoint(
    dataset_id: int,
    report_title: str = "Executive Intelligence Report",
    db: Session = Depends(get_db)
):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    path = ds.cleaned_file_path or ds.file_path
    filename = f"report_{ds.id}_{os.urandom(3).hex()}.pdf"
    out_path = os.path.join(settings.EXPORT_DIR, filename)
    
    generate_pdf_report(path, out_path, report_title=report_title)
    
    return {
        "filename": filename,
        "download_url": f"{settings.API_V1_STR}/reports/download/{filename}",
        "message": "PDF Executive Report generated successfully."
    }

@router.post("/generate-excel/{dataset_id}")
def generate_excel_endpoint(dataset_id: int, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    path = ds.cleaned_file_path or ds.file_path
    filename = f"report_{ds.id}_{os.urandom(3).hex()}.xlsx"
    out_path = os.path.join(settings.EXPORT_DIR, filename)
    
    generate_excel_report(path, out_path, transformation_log=ds.transformation_log)
    
    return {
        "filename": filename,
        "download_url": f"{settings.API_V1_STR}/reports/download/{filename}",
        "message": "Excel Executive Report generated successfully."
    }

@router.get("/download/{filename}")
def download_report_file(filename: str):
    file_path = os.path.join(settings.EXPORT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report file not found")
        
    media_type = "application/pdf" if filename.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return FileResponse(file_path, filename=filename, media_type=media_type)
