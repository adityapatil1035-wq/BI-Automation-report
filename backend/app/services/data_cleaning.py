import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from app.services.data_ingestion import load_dataframe

def clean_dataset(
    file_path: str,
    output_cleaned_path: str,
    impute_missing: bool = True,
    remove_duplicates: bool = True,
    handle_outliers: bool = True,
    date_parsing: bool = True
) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
    
    df = load_dataframe(file_path)
    transformation_log = []
    step_counter = 1
    
    initial_rows = len(df)
    
    # 1. Remove duplicate records
    if remove_duplicates:
        dup_count = int(df.duplicated().sum())
        if dup_count > 0:
            df = df.drop_duplicates().reset_index(drop=True)
            transformation_log.append({
                "step": step_counter,
                "action": "Remove Duplicates",
                "detail": f"Removed {dup_count} duplicate row(s). Dataset reduced from {initial_rows} to {len(df)} rows."
            })
            step_counter += 1

    # 2. Date parsing & standard formatting
    if date_parsing:
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
            elif df[col].dtype == "object":
                non_nulls = df[col].dropna().astype(str)
                if len(non_nulls) > 0:
                    try:
                        parsed = pd.to_datetime(non_nulls, errors="coerce", format="mixed")
                        if parsed.notna().sum() > len(non_nulls) * 0.7:
                            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")
                            transformation_log.append({
                                "step": step_counter,
                                "column": str(col),
                                "action": "Date Standardisation",
                                "detail": f"Parsed and standardized column '{col}' to ISO date format (YYYY-MM-DD)."
                            })
                            step_counter += 1
                    except Exception:
                        pass

    # 3. Missing values imputation
    if impute_missing:
        for col in df.columns:
            missing_count = int(df[col].isna().sum())
            if missing_count > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    median_val = float(df[col].median())
                    if np.isnan(median_val):
                        median_val = 0.0
                    df[col] = df[col].fillna(median_val)
                    transformation_log.append({
                        "step": step_counter,
                        "column": str(col),
                        "action": "Missing Value Imputation",
                        "detail": f"Replaced {missing_count} missing value(s) in numeric column '{col}' using median imputation ({round(median_val, 2)})."
                    })
                    step_counter += 1
                else:
                    mode_series = df[col].mode()
                    fill_val = str(mode_series.iloc[0]) if len(mode_series) > 0 else "Unknown"
                    df[col] = df[col].fillna(fill_val)
                    transformation_log.append({
                        "step": step_counter,
                        "column": str(col),
                        "action": "Missing Value Imputation",
                        "detail": f"Replaced {missing_count} missing value(s) in categorical column '{col}' with mode/default ('{fill_val}')."
                    })
                    step_counter += 1

    # 4. Outlier Handling via IQR Winsorization
    if handle_outliers:
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() > 10:
                # Exclude ID or year columns
                col_name_lower = str(col).lower()
                if "id" in col_name_lower or "year" in col_name_lower or "zip" in col_name_lower:
                    continue
                
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                if iqr > 0:
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    
                    outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                    outlier_count = int(outliers_mask.sum())
                    
                    if outlier_count > 0:
                        df[col] = np.clip(df[col], lower_bound, upper_bound)
                        transformation_log.append({
                            "step": step_counter,
                            "column": str(col),
                            "action": "Outlier Capping (IQR)",
                            "detail": f"Capped {outlier_count} extreme outlier(s) in '{col}' to valid IQR bounds [{round(lower_bound, 2)}, {round(upper_bound, 2)}]."
                        })
                        step_counter += 1

    # Save cleaned file
    os.makedirs(os.path.dirname(output_cleaned_path), exist_ok=True)
    df.to_csv(output_cleaned_path, index=False)
    
    # Calculate new data quality score
    new_rows = len(df)
    new_cols = len(df.columns)
    new_missing = int(df.isna().sum().sum())
    new_dup = int(df.duplicated().sum())
    
    cleaned_quality_score = 100.0 if (new_missing == 0 and new_dup == 0) else round(max(0.0, 100.0 - (new_missing * 1.5) - (new_dup * 2.0)), 1)
    
    summary = {
        "initial_rows": initial_rows,
        "cleaned_rows": new_rows,
        "columns": new_cols,
        "cleaned_quality_score": cleaned_quality_score,
        "transformations_applied": len(transformation_log)
    }
    
    return output_cleaned_path, transformation_log, summary
