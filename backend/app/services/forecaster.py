import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from app.services.data_ingestion import load_dataframe

def generate_time_series_forecast(
    file_path: str,
    date_column: str = None,
    value_column: str = None,
    horizon_days: int = 30,
    model_type: str = "auto"
) -> Dict[str, Any]:
    
    df = load_dataframe(file_path)
    
    if len(df) == 0:
        return {"historical": [], "forecast": [], "model_name": "None", "metrics": {}}

    cols_map = {str(c).lower(): c for c in df.columns}
    
    # Auto detect date & value columns if not provided
    if not date_column:
        for kw in ["date", "order_date", "time", "created_at"]:
            for c_lower, orig in cols_map.items():
                if kw in c_lower:
                    date_column = orig
                    break
            if date_column:
                break
                
    if not value_column:
        for kw in ["sales", "revenue", "amount", "profit", "quantity"]:
            for c_lower, orig in cols_map.items():
                if kw in c_lower:
                    value_column = orig
                    break
            if value_column:
                break

    if not date_column or not value_column or value_column not in df.columns:
        return {"historical": [], "forecast": [], "model_name": "Invalid Columns", "metrics": {}}

    # Prepare historical daily aggregation
    df_temp = df[[date_column, value_column]].copy()
    df_temp[date_column] = pd.to_datetime(df_temp[date_column], errors='coerce')
    df_temp = df_temp.dropna(subset=[date_column]).sort_values(by=date_column)
    
    daily_df = df_temp.groupby(pd.Grouper(key=date_column, freq='D')).agg({value_column: 'sum'}).reset_index()
    daily_df = daily_df.sort_values(by=date_column).reset_index(drop=True)
    
    if len(daily_df) < 7:
        return {"historical": [], "forecast": [], "model_name": "Insufficient Data", "metrics": {}}

    daily_df['day_idx'] = np.arange(len(daily_df))
    daily_df['y'] = daily_df[value_column].astype(float)
    
    X = daily_df[['day_idx']].values
    y = daily_df['y'].values
    
    # Select Model
    if model_type == "random_forest" and len(daily_df) > 30:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model_name = "Random Forest Regressor"
    elif model_type == "ridge":
        model = Ridge(alpha=1.0)
        model_name = "Ridge Linear Regression"
    else:
        model = LinearRegression()
        model_name = "Linear Trend Model"

    model.fit(X, y)
    y_pred = model.predict(X)
    
    # Calculate fit metrics
    rmse = float(np.sqrt(mean_squared_error(y, y_pred)))
    mae = float(mean_absolute_error(y, y_pred))
    r2 = float(r2_score(y, y_pred)) if len(y) > 1 else 0.0
    
    # Generate Forecast for future horizon
    last_date = daily_df[date_column].max()
    last_idx = daily_df['day_idx'].max()
    
    future_indices = np.arange(last_idx + 1, last_idx + 1 + horizon_days).reshape(-1, 1)
    future_preds = model.predict(future_indices)
    
    # Residual standard deviation for confidence interval
    residuals = y - y_pred
    std_residual = float(np.std(residuals)) if len(residuals) > 0 else (np.mean(y) * 0.1)
    
    historical_out = []
    for _, row in daily_df.iterrows():
        historical_out.append({
            "date": row[date_column].strftime("%Y-%m-%d"),
            "actual": round(float(row['y']), 2)
        })
        
    forecast_out = []
    for i, f_idx in enumerate(future_indices.flatten()):
        f_date = last_date + timedelta(days=i+1)
        pred_val = float(future_preds[i])
        
        # Add slight trend noise / confidence expansion
        uncertainty = std_residual * 1.96 * np.sqrt(1 + (i / horizon_days))
        upper_bound = max(0.0, pred_val + uncertainty)
        lower_bound = max(0.0, pred_val - uncertainty)
        
        forecast_out.append({
            "date": f_date.strftime("%Y-%m-%d"),
            "forecast": round(pred_val, 2),
            "upper_bound": round(upper_bound, 2),
            "lower_bound": round(lower_bound, 2)
        })

    return {
        "historical": historical_out[-60:],  # last 60 days historical
        "forecast": forecast_out,
        "model_name": model_name,
        "horizon_days": horizon_days,
        "metrics": {
            "rmse": round(rmse, 2),
            "mae": round(mae, 2),
            "r2_score": round(r2, 3),
            "target_column": str(value_column),
            "date_column": str(date_column)
        }
    }
