import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.api import auth, datasets, dashboards, analytics, forecasting, nl_query, reports, schedules, connectors
from app.services.scheduler_service import start_scheduler, shutdown_scheduler
from app.models.all_models import Workspace, User, Dataset
from app.services.data_ingestion import analyze_dataset_structure
from app.services.domain_detector import detect_business_domain
from app.services.data_ingestion import load_dataframe

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(datasets.router, prefix=settings.API_V1_STR)
app.include_router(dashboards.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(forecasting.router, prefix=settings.API_V1_STR)
app.include_router(nl_query.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)
app.include_router(schedules.router, prefix=settings.API_V1_STR)
app.include_router(connectors.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def on_startup():
    start_scheduler()
    
    # Auto-seed database with Retail Sales Demo data if empty
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            from app.core.security import get_password_hash
            ws = Workspace(name="Acme Corp Workspace", description="Primary Enterprise Analytics Workspace")
            db.add(ws)
            db.commit()
            db.refresh(ws)
            
            admin_user = User(
                email="admin@acme.com",
                full_name="Alex Mercer (Admin)",
                hashed_password=get_password_hash("admin123"),
                role="Admin",
                workspace_id=ws.id
            )
            db.add(admin_user)
            db.commit()

            demo_path = os.path.abspath("../data/retail_sales_demo.csv")
            if not os.path.exists(demo_path):
                demo_path = os.path.abspath("./data/retail_sales_demo.csv")

            if os.path.exists(demo_path):
                profile = analyze_dataset_structure(demo_path)
                df = load_dataframe(demo_path)
                dom, _, _ = detect_business_domain(df)
                
                ds = Dataset(
                    name="Retail Sales Analytics Demo",
                    filename="retail_sales_demo.csv",
                    file_path=demo_path,
                    file_type="csv",
                    row_count=profile["row_count"],
                    col_count=profile["col_count"],
                    data_quality_score=profile["data_quality_score"],
                    domain=dom,
                    quality_summary=profile["quality_summary"],
                    column_metadata=profile["column_metadata"],
                    workspace_id=ws.id
                )
                db.add(ds)
                db.commit()
                print("[STARTUP SEED] Successfully auto-seeded demo dataset into database.")
    except Exception as e:
        print(f"[STARTUP SEED WARNING] Could not auto-seed database: {e}")
    finally:
        db.close()

@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()

@app.get("/")
def root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs"
    }
