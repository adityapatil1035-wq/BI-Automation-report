from datetime import datetime
import json
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="workspace")
    datasets = relationship("Dataset", back_populates="workspace")
    dashboards = relationship("Dashboard", back_populates="workspace")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="Analyst")  # Admin, Analyst, Viewer
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspace = relationship("Workspace", back_populates="users")

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    cleaned_file_path = Column(String(500), nullable=True)
    file_type = Column(String(20), nullable=False)
    row_count = Column(Integer, default=0)
    col_count = Column(Integer, default=0)
    data_quality_score = Column(Float, default=100.0)
    domain = Column(String(50), default="Sales")
    
    quality_summary = Column(JSON, nullable=True)
    transformation_log = Column(JSON, nullable=True)
    column_metadata = Column(JSON, nullable=True)
    
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspace = relationship("Workspace", back_populates="datasets")
    dashboards = relationship("Dashboard", back_populates="dataset")

class Dashboard(Base):
    __tablename__ = "dashboards"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    domain = Column(String(50), default="Sales")
    layout_config = Column(JSON, nullable=True)
    
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dataset = relationship("Dataset", back_populates="dashboards")
    workspace = relationship("Workspace", back_populates="dashboards")

class ReportSchedule(Base):
    __tablename__ = "report_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    report_type = Column(String(50), default="Daily")  # Daily, Weekly, Monthly
    frequency = Column(String(50), default="Daily")
    time_of_day = Column(String(20), default="09:00")
    day_of_week = Column(String(20), default="Monday")
    recipients = Column(Text, nullable=False)  # Comma separated emails
    format = Column(String(20), default="PDF")  # PDF, Excel, Both
    
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"), nullable=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)
    
    is_active = Column(Boolean, default=True)
    last_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
