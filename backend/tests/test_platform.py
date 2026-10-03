import os
import pytest
from app.services.data_ingestion import analyze_dataset_structure, load_dataframe
from app.services.data_cleaning import clean_dataset
from app.services.domain_detector import detect_business_domain
from app.services.kpi_engine import compute_dataset_kpis
from app.services.dashboard_generator import generate_dashboard_specs
from app.services.insight_engine import generate_ai_business_insights
from app.services.anomaly_detector import detect_anomalies_in_dataset
from app.services.forecaster import generate_time_series_forecast
from app.services.nl_bi_engine import process_natural_language_query
from app.services.pdf_report_generator import generate_pdf_report
from app.services.excel_report_generator import generate_excel_report

DEMO_PATH = os.path.abspath("data/retail_sales_demo.csv")

def test_data_ingestion_and_profiling():
    assert os.path.exists(DEMO_PATH), "Demo dataset file should exist"
    profile = analyze_dataset_structure(DEMO_PATH)
    assert profile["row_count"] >= 1000
    assert profile["col_count"] >= 10
    assert profile["data_quality_score"] > 80.0
    assert "Sales" in profile["column_metadata"]

def test_domain_detection():
    df = load_dataframe(DEMO_PATH)
    domain, confidence, scores = detect_business_domain(df)
    assert domain in ["Sales", "Retail", "E-commerce"]
    assert confidence > 50.0

def test_kpi_engine():
    res = compute_dataset_kpis(DEMO_PATH)
    kpis = res["kpis"]
    assert len(kpis) >= 4
    total_rev_kpi = next((k for k in kpis if k["id"] == "total_revenue"), None)
    assert total_rev_kpi is not None
    assert total_rev_kpi["raw_value"] > 0

def test_dashboard_generator():
    specs = generate_dashboard_specs(DEMO_PATH)
    assert len(specs["widgets"]) >= 4
    assert len(specs["filters"]) >= 2

def test_ai_insights():
    insights = generate_ai_business_insights(DEMO_PATH)
    assert len(insights) >= 2

def test_anomaly_detection():
    anomalies = detect_anomalies_in_dataset(DEMO_PATH)
    assert isinstance(anomalies, list)
    assert len(anomalies) > 0

def test_forecasting():
    res = generate_time_series_forecast(DEMO_PATH, horizon_days=30)
    assert len(res["forecast"]) == 30
    assert "rmse" in res["metrics"]

def test_ask_your_data():
    nl_res = process_natural_language_query(DEMO_PATH, "Show me sales for West region")
    assert "West" in nl_res["answer"]
    assert len(nl_res["table_data"]) > 0

def test_pdf_report_generation(tmp_path):
    pdf_out = os.path.join(tmp_path, "test_report.pdf")
    res_path = generate_pdf_report(DEMO_PATH, pdf_out)
    assert os.path.exists(res_path)
    assert os.path.getsize(res_path) > 1000

def test_excel_report_generation(tmp_path):
    excel_out = os.path.join(tmp_path, "test_report.xlsx")
    res_path = generate_excel_report(DEMO_PATH, excel_out)
    assert os.path.exists(res_path)
    assert os.path.getsize(res_path) > 1000
