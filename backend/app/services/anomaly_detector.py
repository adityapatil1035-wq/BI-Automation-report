import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import IsolationForest
from app.services.data_ingestion import load_dataframe

def detect_anomalies_in_dataset(file_path: str, z_threshold: float = 2.5) -> List[Dict[str, Any]]:
    df = load_dataframe(file_path)
    
    if len(df) == 0:
        return []

    cols_map = {str(c).lower(): c for c in df.columns}
    
    def find_col(keywords: List[str]):
        for kw in keywords:
            for c_lower, orig in cols_map.items():
                if kw in c_lower:
                    return orig
        return None

    sales_col = find_col(["sales", "revenue", "amount"])
    profit_col = find_col(["profit", "margin"])
    date_col = find_col(["date", "order_date", "created_at"])
    product_col = find_col(["product", "item"])
    region_col = find_col(["region", "city"])

    target_cols = []
    if sales_col and pd.api.types.is_numeric_dtype(df[sales_col]):
        target_cols.append(sales_col)
    if profit_col and pd.api.types.is_numeric_dtype(df[profit_col]):
        target_cols.append(profit_col)

    if not target_cols:
        return []

    anomalies = []
    anom_counter = 1

    for target in target_cols:
        series = df[target].dropna()
        if len(series) < 10:
            continue
            
        mean_val = float(series.mean())
        std_val = float(series.std())
        
        if std_val == 0:
            continue

        # 1. Z-Score approach
        z_scores = (df[target] - mean_val) / std_val
        
        # 2. Isolation Forest for multi-feature or single feature validation
        try:
            X = df[[target]].fillna(mean_val).values
            iso = IsolationForest(contamination=0.03, random_state=42)
            preds = iso.fit_predict(X)
        except Exception:
            preds = np.ones(len(df))

        for idx, z in z_scores.items():
            if abs(z) >= z_threshold or preds[idx] == -1:
                val = float(df.loc[idx, target])
                diff_pct = round(((val - mean_val) / mean_val) * 100.0, 1) if mean_val != 0 else 0.0
                
                anom_type = "Spike (Surge)" if val > mean_val else "Drop (Contraction)"
                severity = "Critical" if abs(z) >= 3.5 else ("High" if abs(z) >= 2.8 else "Medium")
                
                date_str = str(df.loc[idx, date_col]) if date_col and date_col in df.columns else f"Row #{idx+1}"
                prod_str = str(df.loc[idx, product_col]) if product_col and product_col in df.columns else "N/A"
                reg_str = str(df.loc[idx, region_col]) if region_col and region_col in df.columns else "N/A"
                
                anomalies.append({
                    "id": f"anom_{anom_counter}",
                    "row_index": int(idx),
                    "date": date_str,
                    "metric_name": str(target),
                    "actual_value": round(val, 2),
                    "expected_value": round(mean_val, 2),
                    "z_score": round(float(z), 2),
                    "anomaly_type": anom_type,
                    "severity": severity,
                    "product": prod_str,
                    "region": reg_str,
                    "description": f"Unusual {target} {anom_type.lower()} detected on {date_str}. Actual value of ₹{val:,.2f} is {diff_pct:+}% relative to dataset average (₹{mean_val:,.2f})."
                })
                anom_counter += 1

    # Sort by severity and z_score magnitude
    anomalies.sort(key=lambda x: abs(x["z_score"]), reverse=True)
    return anomalies[:20]  # Return top 20 anomalies
