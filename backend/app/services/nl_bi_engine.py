import pandas as pd
import numpy as np
import re
import json
from typing import Dict, Any, List
from app.services.data_ingestion import load_dataframe

def process_natural_language_query(file_path: str, user_query: str) -> Dict[str, Any]:
    df = load_dataframe(file_path)
    
    if len(df) == 0:
        return {
            "answer": "Dataset is empty.",
            "chart_type": None,
            "chart_data": [],
            "table_data": [],
            "sql_or_pandas_query": "df.head(0)"
        }

    q_lower = user_query.lower()
    cols_map = {str(c).lower(): c for c in df.columns}
    
    def find_col(keywords: List[str]):
        for kw in keywords:
            for c_lower, orig in cols_map.items():
                if kw in c_lower:
                    return orig
        return None

    sales_col = find_col(["sales", "revenue", "amount"])
    profit_col = find_col(["profit", "margin"])
    qty_col = find_col(["quantity", "qty", "units"])
    cost_col = find_col(["cost", "expense"])
    region_col = find_col(["region", "location", "state", "city"])
    category_col = find_col(["category", "department", "type"])
    product_col = find_col(["product", "item", "sku"])
    customer_col = find_col(["customer", "client", "user"])
    date_col = find_col(["date", "time", "created_at"])

    def sanitize_table(records):
        if records is None:
            return []
        if isinstance(records, pd.DataFrame):
            if records.empty:
                return []
            return json.loads(records.to_json(orient="records", date_format="iso"))
        if isinstance(records, list):
            if not records:
                return []
            return json.loads(pd.DataFrame(records).to_json(orient="records", date_format="iso"))
        return []

    # 1. Check for specific region filter (e.g. "sales for West", "sales in Gujarat")
    if region_col:
        unique_regions = df[region_col].dropna().unique().tolist()
        for reg in unique_regions:
            if str(reg).lower() in q_lower:
                filtered_df = df[df[region_col].astype(str).str.lower() == str(reg).lower()]
                target_metric = sales_col if sales_col else (profit_col if profit_col else df.columns[0])
                
                if pd.api.types.is_numeric_dtype(filtered_df[target_metric]):
                    total_val = float(filtered_df[target_metric].sum())
                    ans = f"Total {target_metric} for **{reg}** is **${total_val:,.2f}** across {len(filtered_df)} recorded orders."
                else:
                    ans = f"Found {len(filtered_df)} records matching **{reg}**."

                # Group by Category or Product for supporting chart
                chart_data = []
                chart_type = "bar"
                if category_col and sales_col:
                    grp = filtered_df.groupby(category_col)[sales_col].sum().reset_index()
                    chart_data = [{"category": str(r[category_col]), "Sales": round(float(r[sales_col]), 2)} for _, r in grp.iterrows()]
                
                table_data = sanitize_table(filtered_df.head(15))
                return {
                    "answer": ans,
                    "chart_type": chart_type,
                    "chart_data": chart_data,
                    "table_data": table_data,
                    "columns": list(filtered_df.columns),
                    "sql_or_pandas_query": f"df[df['{region_col}'] == '{reg}'].agg({{'{target_metric}': 'sum'}})"
                }

    # 2. Check for Top Products / Customers query (e.g. "top 10 products", "highest profit")
    if "top" in q_lower or "highest" in q_lower or "best" in q_lower:
        # Determine limit (e.g., top 10, top 5)
        top_n = 10
        match_n = re.search(r'\btop\s+(\d+)', q_lower)
        if match_n:
            top_n = int(match_n.group(1))

        dim_col = product_col if "product" in q_lower else (customer_col if "customer" in q_lower else (category_col if "category" in q_lower else product_col))
        val_col = profit_col if "profit" in q_lower else (sales_col if sales_col else profit_col)
        
        if dim_col and val_col and pd.api.types.is_numeric_dtype(df[val_col]):
            top_df = df.groupby(dim_col)[val_col].sum().reset_index().sort_values(by=val_col, ascending=False).head(top_n)
            top_item = str(top_df.iloc[0][dim_col])
            top_val = float(top_df.iloc[0][val_col])
            
            ans = f"The highest performing {dim_col} is **{top_item}** with total {val_col} of **${top_val:,.2f}**. Here are the Top {len(top_df)} items:"
            
            chart_data = [{"name": str(r[dim_col]), "value": round(float(r[val_col]), 2)} for _, r in top_df.iterrows()]
            table_data = sanitize_table(top_df)
            
            return {
                "answer": ans,
                "chart_type": "bar",
                "chart_data": chart_data,
                "table_data": table_data,
                "columns": [dim_col, val_col],
                "sql_or_pandas_query": f"df.groupby('{dim_col}')['{val_col}'].sum().nlargest({top_n})"
            }

    # 3. Category Breakdown Query (e.g. "sales by category", "revenue by region")
    if "by category" in q_lower or "by region" in q_lower or "breakdown" in q_lower:
        dim_col = category_col if "category" in q_lower else (region_col if "region" in q_lower else category_col)
        val_col = sales_col if sales_col else profit_col
        
        if dim_col and val_col:
            grp_df = df.groupby(dim_col)[val_col].sum().reset_index().sort_values(by=val_col, ascending=False)
            chart_data = [{"name": str(r[dim_col]), "value": round(float(r[val_col]), 2)} for _, r in grp_df.iterrows()]
            
            ans = f"Here is the breakdown of **{val_col}** grouped by **{dim_col}** across all records:"
            return {
                "answer": ans,
                "chart_type": "donut",
                "chart_data": chart_data,
                "table_data": sanitize_table(grp_df),
                "columns": [dim_col, val_col],
                "sql_or_pandas_query": f"df.groupby('{dim_col}')['{val_col}'].sum()"
            }

    # 4. Default Summary Fallback Query
    val_col = sales_col if sales_col else (profit_col if profit_col else df.columns[0])
    if pd.api.types.is_numeric_dtype(df[val_col]):
        total_val = float(df[val_col].sum())
        mean_val = float(df[val_col].mean())
        ans = f"Based on your query, total **{val_col}** is **${total_val:,.2f}** with an average of **${mean_val:,.2f}** per entry across {len(df):,} records."
    else:
        ans = f"Analyzed dataset containing {len(df):,} total records and {len(df.columns)} columns."

    preview_df = df.head(10)
    chart_data = []
    if category_col and sales_col:
        grp = df.groupby(category_col)[sales_col].sum().reset_index().head(6)
        chart_data = [{"name": str(r[category_col]), "value": round(float(r[sales_col]), 2)} for _, r in grp.iterrows()]

    return {
        "answer": ans,
        "chart_type": "bar" if chart_data else None,
        "chart_data": chart_data,
        "table_data": sanitize_table(preview_df),
        "columns": list(df.columns),
        "sql_or_pandas_query": f"df.describe()"
    }
