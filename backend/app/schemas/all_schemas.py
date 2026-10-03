from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Auth & User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Optional[str] = "Analyst"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    workspace_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

# Workspace Schemas
class WorkspaceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class WorkspaceOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Dataset Schemas
class DatasetOut(BaseModel):
    id: int
    name: str
    filename: str
    file_type: str
    row_count: int
    col_count: int
    data_quality_score: float
    domain: str
    quality_summary: Optional[Dict[str, Any]] = None
    transformation_log: Optional[List[Dict[str, Any]]] = None
    column_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CleanDatasetRequest(BaseModel):
    impute_missing: bool = True
    remove_duplicates: bool = True
    handle_outliers: bool = True
    date_parsing: bool = True

# Dashboard Schemas
class WidgetConfig(BaseModel):
    id: str
    title: str
    chart_type: str  # kpi_card, line, bar, donut, area, scatter, heatmap, table
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    category_col: Optional[str] = None
    aggregation: Optional[str] = "sum"  # sum, avg, count, min, max
    w: Optional[int] = 6
    h: Optional[int] = 4

class DashboardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    domain: Optional[str] = "Sales"
    dataset_id: int
    layout_config: Optional[Dict[str, Any]] = None

class DashboardOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    domain: str
    dataset_id: int
    layout_config: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Ask Your Data NL Query Schema
class NLQueryRequest(BaseModel):
    dataset_id: int
    query: str

class NLQueryResponse(BaseModel):
    answer: str
    chart_type: Optional[str] = None
    chart_data: Optional[List[Dict[str, Any]]] = None
    table_data: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    sql_or_pandas_query: Optional[str] = None

# Forecast Request & Response Schemas
class ForecastRequest(BaseModel):
    dataset_id: int
    date_column: str
    value_column: str
    horizon_days: int = 30  # 7, 30, 90, 180
    model_type: str = "auto"  # auto, linear, random_forest, moving_average

class ForecastResponse(BaseModel):
    historical: List[Dict[str, Any]]
    forecast: List[Dict[str, Any]]
    model_name: str
    metrics: Dict[str, Any]

# Schedule Schemas
class ScheduleCreate(BaseModel):
    title: str
    report_type: str = "Daily"  # Daily, Weekly, Monthly
    frequency: str = "Daily"
    time_of_day: str = "09:00"
    day_of_week: str = "Monday"
    recipients: str
    format: str = "PDF"
    dataset_id: int
    dashboard_id: Optional[int] = None

class ScheduleOut(ScheduleCreate):
    id: int
    is_active: bool
    last_run_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
