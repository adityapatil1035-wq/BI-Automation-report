export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'Admin' | 'Analyst' | 'Viewer';
  workspace_id?: number;
  is_active: boolean;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface Dataset {
  id: number;
  name: string;
  filename: string;
  file_type: string;
  row_count: number;
  col_count: number;
  data_quality_score: number;
  domain: string;
  quality_summary?: {
    data_quality_score: number;
    rows: number;
    columns: number;
    missing_cells: number;
    missing_percentage: number;
    duplicate_rows: number;
    duplicate_percentage: number;
    date_columns: string[];
    numeric_columns: string[];
    categorical_columns: string[];
  };
  transformation_log?: Array<{
    step: number;
    column?: string;
    action: string;
    detail: string;
  }>;
  column_metadata?: Record<string, {
    type: string;
    missing_count: number;
    missing_pct: number;
    unique_values: number;
    sample_values: string[];
  }>;
  created_at: string;
}

export interface KPI {
  id: string;
  name: string;
  value: string;
  raw_value: number;
  unit: string;
  trend: string;
  status: 'positive' | 'negative' | 'neutral' | 'warning';
}

export interface Widget {
  id: string;
  title: string;
  type: 'kpi_cards' | 'line' | 'bar' | 'donut' | 'area' | 'scatter' | 'heatmap' | 'table';
  x_axis?: string | string[];
  y_axis?: string | string[];
  data: any[];
  w?: number;
  h?: number;
}

export interface Dashboard {
  id: number;
  title: string;
  description?: string;
  domain: string;
  dataset_id: number;
  layout_config?: {
    title: string;
    domain: string;
    kpis: KPI[];
    widgets: Widget[];
    filters: Array<{
      id: string;
      label: string;
      type: string;
      column: string;
      options?: string[];
    }>;
  };
  created_at: string;
}

export interface Insight {
  id: string;
  title: string;
  category: string;
  type: 'positive' | 'negative' | 'neutral' | 'warning';
  metric: string;
  impact: string;
  description: string;
  recommendation: string;
}

export interface Anomaly {
  id: string;
  row_index: number;
  date: string;
  metric_name: string;
  actual_value: number;
  expected_value: number;
  z_score: number;
  anomaly_type: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  product: string;
  region: string;
  description: string;
}

export interface ForecastData {
  historical: Array<{ date: string; actual: number }>;
  forecast: Array<{ date: string; forecast: number; upper_bound: number; lower_bound: number }>;
  model_name: string;
  horizon_days: number;
  metrics: {
    rmse: number;
    mae: number;
    r2_score: number;
    target_column: string;
    date_column: string;
  };
}

export interface ReportSchedule {
  id: number;
  title: string;
  report_type: string;
  frequency: string;
  time_of_day: string;
  day_of_week: string;
  recipients: string;
  format: string;
  dataset_id: number;
  dashboard_id?: number;
  is_active: boolean;
  last_run_at?: string;
  created_at: string;
}

export interface NLQueryResponse {
  answer: string;
  chart_type?: string;
  chart_data?: any[];
  table_data?: any[];
  columns?: string[];
  sql_or_pandas_query?: string;
}
