from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.all_models import ReportSchedule, Dataset
from app.schemas.all_schemas import ScheduleCreate, ScheduleOut
from app.services.scheduler_service import run_scheduled_report_job

router = APIRouter(prefix="/schedules", tags=["Report Scheduler"])

@router.post("", response_model=ScheduleOut)
def create_schedule(schedule_in: ScheduleCreate, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == schedule_in.dataset_id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    sched = ReportSchedule(
        title=schedule_in.title,
        report_type=schedule_in.report_type,
        frequency=schedule_in.frequency,
        time_of_day=schedule_in.time_of_day,
        day_of_week=schedule_in.day_of_week,
        recipients=schedule_in.recipients,
        format=schedule_in.format,
        dataset_id=schedule_in.dataset_id,
        dashboard_id=schedule_in.dashboard_id,
        workspace_id=1
    )
    
    db.add(sched)
    db.commit()
    db.refresh(sched)
    
    return sched

@router.get("", response_model=List[ScheduleOut])
def list_schedules(db: Session = Depends(get_db)):
    return db.query(ReportSchedule).order_by(ReportSchedule.created_at.desc()).all()

@router.post("/{schedule_id}/trigger")
def trigger_schedule_now(schedule_id: int, db: Session = Depends(get_db)):
    sched = db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).first()
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
        
    ds = db.query(Dataset).filter(Dataset.id == sched.dataset_id).first()
    path = ds.cleaned_file_path or ds.file_path
    
    run_scheduled_report_job(
        schedule_id=sched.id,
        title=sched.title,
        file_path=path,
        recipients_str=sched.recipients,
        format_type=sched.format
    )
    
    return {"message": f"Successfully triggered report schedule '{sched.title}'"}
