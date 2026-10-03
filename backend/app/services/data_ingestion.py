import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List

def load_dataframe(file_path: str, file_type: str = None) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower() if not file_type else f".{file_type.lower()}"
    
    if ext in ['.csv', 'csv']:
        return pd.read_csv(file_path)
    elif ext in ['.xlsx', '.xls', 'xlsx', 'xls']:
        try:
            return pd.read_excel(file_path)
        except Exception:
            return pd.read_csv(file_path)
    elif ext in ['.json', 'json']:
        return pd.read_json(file_path)
    else:
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.read_excel(file_path)

def analyze_dataset_structure(file_path: str) -> Dict[str, Any]:
    df = load_dataframe(file_path)
    
    total_rows = len(df)
    total_cols = len(df.columns)
    
    if total_rows == 0:
        return {
            "row_count": 0,
            "col_count": 0,
            "data_quality_score": 0.0,
            "quality_summary": {"error": "Dataset is empty"},
            "column_metadata": {}
        }
    
    # Missing & duplicate counts
    total_cells = total_rows * total_cols
    missing_cells = int(df.isna().sum().sum())
    missing_pct = round((missing_cells / total_cells) * 100, 2) if total_cells > 0 else 0.0
    
    duplicate_rows = int(df.duplicated().sum())
    duplicate_pct = round((duplicate_rows / total_rows) * 100, 2)
    
    column_metadata = {}
    date_cols = []
    numeric_cols = []
    categorical_cols = []
    
    for col in df.columns:
        col_str = str(col)
        col_data = df[col]
        col_missing = int(col_data.isna().sum())
        col_missing_pct = round((col_missing / total_rows) * 100, 2)
        
        # Check if datetime
        is_date = False
        if pd.api.types.is_datetime64_any_dtype(col_data):
            is_date = True
        elif col_data.dtype == 'object':
            # Try parsing a small sample
            non_nulls = col_data.dropna().astype(str)
            if len(non_nulls) > 0:
                sample = non_nulls.head(20)
                try:
                    parsed = pd.to_datetime(sample, errors='coerce', format='mixed')
                    if parsed.notna().sum() > len(sample) * 0.7:
                        is_date = True
                except Exception:
                    pass
                    
        if is_date:
            date_cols.append(col_str)
            col_type = "datetime"
        elif pd.api.types.is_numeric_dtype(col_data):
            numeric_cols.append(col_str)
            col_type = "numeric"
        else:
            categorical_cols.append(col_str)
            col_type = "categorical"
            
        column_metadata[col_str] = {
            "type": col_type,
            "missing_count": col_missing,
            "missing_pct": col_missing_pct,
            "unique_values": int(col_data.nunique()),
            "sample_values": [str(x) for x in col_data.dropna().head(3).tolist()]
        }
        
    # Calculate Data Quality Score (0 to 100)
    # Deductions: missing cell % * 1.5, duplicate row % * 2.0
    quality_score = max(0.0, min(100.0, 100.0 - (missing_pct * 1.5) - (duplicate_pct * 2.0)))
    quality_score = round(quality_score, 1)
    
    quality_summary = {
        "data_quality_score": quality_score,
        "rows": total_rows,
        "columns": total_cols,
        "missing_cells": missing_cells,
        "missing_percentage": missing_pct,
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": duplicate_pct,
        "date_columns": date_cols,
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "date_columns_count": len(date_cols),
        "numeric_columns_count": len(numeric_cols),
        "categorical_columns_count": len(categorical_cols)
    }
    
    return {
        "row_count": total_rows,
        "col_count": total_cols,
        "data_quality_score": quality_score,
        "quality_summary": quality_summary,
        "column_metadata": column_metadata
    }
