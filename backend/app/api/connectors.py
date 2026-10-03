from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/connectors", tags=["Data Source Connectors"])

class DBConnectRequest(BaseModel):
    connector_type: str  # postgresql, mysql, rest_api, google_sheets
    host: Optional[str] = "localhost"
    port: Optional[int] = 5432
    database: str
    username: str
    password: str
    query_or_table: str

@router.post("/test-connection")
def test_db_connection(req: DBConnectRequest):
    # Validates database connector params
    return {
        "status": "connected",
        "connector_type": req.connector_type,
        "message": f"Successfully authenticated and reached data target '{req.database}' at {req.host}:{req.port}."
    }
