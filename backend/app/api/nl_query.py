from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.all_models import Dataset
from app.schemas.all_schemas import NLQueryRequest, NLQueryResponse
from app.services.nl_bi_engine import process_natural_language_query

router = APIRouter(prefix="/nl-query", tags=["Natural Language BI - Ask Your Data"])

@router.post("/ask", response_model=NLQueryResponse)
def ask_natural_language_query(req: NLQueryRequest, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == req.dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    path = ds.cleaned_file_path or ds.file_path
    return process_natural_language_query(path, req.query)
