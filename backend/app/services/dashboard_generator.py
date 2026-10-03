import pandas as pd
import numpy as np
from typing import Dict, Any, List
from app.services.data_ingestion import load_dataframe
from app.services.kpi_engine import compute_dataset_kpis

def generate_dashboard_specs(file_path: str, domain: str = "Sales") -> Dict[str, Any]:
    df = load_dataframe(file_path)
    
    if len(df) == 0:
        return {"widgets": [], "filters": [], "kpis": []}
        
    cols_map = {str(c).lower(): c for c in df.columns}
    
    def find_col(keywords: List[str]):
        for kw in keywords:
            for c_lower, orig in cols_map.items():
                if kw in c_lower:
                    return orig
        return None

    date_col = find_col(["date", "order_date", "time", "created_at"])
    sales_col = find_col(["sales", "revenue", "amount", "total_price"])
    profit_col = find_col(["profit", "margin", "earnings"])
    cost_col = find_col(["cost", "expense"])
    qty_col = find_col(["quantity", "qty", "units"])
    category_col = find_col(["category", "type", "department", "group"])
    region_col = find_col(["region", "location", "area", "zone", "state", "city"])
    product_col = find_col(["product", "item", "sku", "name", "title"])
    segment_col = find_col(["segment", "channel", "customer_type"])

    kpis_data = compute_dataset_kpis(file_path, domain=domain)
    
    widgets = []
    
    # Widget 1: KPI Summary Cards
    widgets.append({
        "id": "w_kpis",
        "title": "Key Executive Metrics",
        "type": "kpi_cards",
        "w": 12,
        "h": 3,
        "data": kpis_data["kpis"]
    })
    
    # Widget 2: Time Series Trend (Line Chart)
    if date_col and sales_col:
        try:
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
            df_temp = df_temp.dropna(subset=[date_col])
            
            # Resample monthly or daily
            df_trend = df_temp.groupby(pd.Grouper(key=date_col, freq='ME')).agg({
                sales_col: 'sum',
                profit_col: 'sum' if profit_col else 'count'
            }).reset_index()
            
            trend_data = []
            for _, row in df_trend.iterrows():
                d_str = row[date_col].strftime("%b %Y")
                item = {
                    "date": d_str,
                    "Sales": round(float(row[sales_col]), 2)
                }
                if profit_col:
                    item["Profit"] = round(float(row[profit_col]), 2)
                trend_data.append(item)
                
            widgets.append({
                "id": "w_trend",
                "title": f"Revenue & Profit Trend ({date_col})",
                "type": "line",
                "x_axis": "date",
                "y_axis": ["Sales", "Profit"] if profit_col else ["Sales"],
                "w": 8,
                "h": 5,
                "data": trend_data
            })
        except Exception:
            pass

    # Widget 3: Category Performance (Bar Chart)
    if category_col and sales_col:
        df_cat = df.groupby(category_col).agg({
            sales_col: 'sum',
            profit_col: 'sum' if profit_col else 'count'
        }).reset_index().sort_values(by=sales_col, ascending=False).head(8)
        
        cat_data = []
        for _, row in df_cat.iterrows():
            item = {
                "category": str(row[category_col]),
                "Sales": round(float(row[sales_col]), 2)
            }
            if profit_col:
                item["Profit"] = round(float(row[profit_col]), 2)
            cat_data.append(item)
            
        widgets.append({
            "id": "w_category",
            "title": f"Performance by Category ({category_col})",
            "type": "bar",
            "x_axis": "category",
            "y_axis": ["Sales", "Profit"] if profit_col else ["Sales"],
            "w": 4,
            "h": 5,
            "data": cat_data
        })

    # Widget 4: Regional Distribution (Donut / Pie Chart)
    if region_col and sales_col:
        df_reg = df.groupby(region_col).agg({sales_col: 'sum'}).reset_index().sort_values(by=sales_col, ascending=False).head(6)
        
        reg_data = []
        for _, row in df_reg.iterrows():
            reg_data.append({
                "name": str(row[region_col]),
                "value": round(float(row[sales_col]), 2)
            })
            
        widgets.append({
            "id": "w_region",
            "title": f"Sales Distribution by Region ({region_col})",
            "type": "donut",
            "x_axis": "name",
            "y_axis": "value",
            "w": 4,
            "h": 5,
            "data": reg_data
        })

    # Widget 5: Top 10 Products (Table Widget)
    if product_col and sales_col:
        agg_dict = {sales_col: 'sum'}
        if qty_col:
            agg_dict[qty_col] = 'sum'
        if profit_col:
            agg_dict[profit_col] = 'sum'
            
        df_prod = df.groupby(product_col).agg(agg_dict).reset_index().sort_values(by=sales_col, ascending=False).head(10)
        
        prod_data = []
        for _, row in df_prod.iterrows():
            item = {
                "product": str(row[product_col]),
                "sales": round(float(row[sales_col]), 2)
            }
            if qty_col:
                item["units"] = int(row[qty_col])
            if profit_col:
                item["profit"] = round(float(row[profit_col]), 2)
            prod_data.append(item)
            
        widgets.append({
            "id": "w_top_products",
            "title": f"Top Performing Products",
            "type": "table",
            "w": 8,
            "h": 5,
            "data": prod_data
        })

    # Widget 6: Segment Profitability (Area / Bar Chart)
    if segment_col and sales_col:
        df_seg = df.groupby(segment_col).agg({
            sales_col: 'sum',
            profit_col: 'sum' if profit_col else 'count'
        }).reset_index()
        
        seg_data = []
        for _, row in df_seg.iterrows():
            item = {
                "segment": str(row[segment_col]),
                "Sales": round(float(row[sales_col]), 2)
            }
            if profit_col:
                item["Profit"] = round(float(row[profit_col]), 2)
            seg_data.append(item)
            
        widgets.append({
            "id": "w_segment",
            "title": f"Revenue by Customer Segment",
            "type": "area",
            "x_axis": "segment",
            "y_axis": ["Sales", "Profit"] if profit_col else ["Sales"],
            "w": 6,
            "h": 5,
            "data": seg_data
        })

    # Dynamic Filter definitions
    filters = []
    if date_col:
        filters.append({"id": "date_range", "label": "Date Range", "type": "date_range", "column": date_col})
    if region_col:
        regions_list = df[region_col].dropna().unique().tolist()
        filters.append({"id": "region", "label": "Region", "type": "select", "column": region_col, "options": regions_list})
    if category_col:
        cats_list = df[category_col].dropna().unique().tolist()
        filters.append({"id": "category", "label": "Category", "type": "select", "column": category_col, "options": cats_list})
    if segment_col:
        segs_list = df[segment_col].dropna().unique().tolist()
        filters.append({"id": "segment", "label": "Segment", "type": "select", "column": segment_col, "options": segs_list})

    return {
        "title": f"Executive {domain} Analytics Dashboard",
        "domain": domain,
        "kpis": kpis_data["kpis"],
        "widgets": widgets,
        "filters": filters
    }
