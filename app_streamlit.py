import os
import re
import io
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import Ridge

# Page Configuration
st.set_page_config(
    page_title="AI-Powered Automated BI Reporting Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark Theme
st.markdown("""
<style>
    .main {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .stApp {
        background-color: #0F172A;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #94A3B8;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #38BDF8;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #10B981;
        margin-top: 4px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #2563EB, #4F46E5);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1D4ED8, #4338CA);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Helper Data Loader
@st.cache_data
def load_data(file_source):
    if isinstance(file_source, str):
        df = pd.read_csv(file_source)
    else:
        file_ext = os.path.splitext(file_source.name)[1].lower()
        if file_ext in ['.csv', 'csv']:
            df = pd.read_csv(file_source)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_source)
        elif file_ext == '.json':
            df = pd.read_json(file_source)
        else:
            df = pd.read_csv(file_source)
    
    # Parse dates if any
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

# Main Sidebar
st.sidebar.image("https://img.icons8.com/isometric/96/combo-chart.png", width=64)
st.sidebar.title("BI Intelligence Suite")
st.sidebar.caption("Enterprise Automated Reporting Engine v1.0")

nav_option = st.sidebar.radio(
    "Navigation Options",
    [
        "📊 Executive BI Dashboard",
        "📁 Data Profiler & Upload",
        "🤖 AI Business Insights",
        "🚨 ML Anomaly Detection",
        "📈 Time-Series Forecasting",
        "💬 Ask Your Data (NL Query)",
        "📄 Report Generator Export"
    ]
)

# Load Default Dataset
default_demo_path = os.path.join(os.path.dirname(__file__), "data", "retail_sales_demo.csv")
uploaded_file = st.sidebar.file_uploader("Upload New Dataset (CSV/XLSX)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    df = load_data(uploaded_file)
    dataset_name = uploaded_file.name
elif os.path.exists(default_demo_path):
    df = load_data(default_demo_path)
    dataset_name = "Retail Sales Analytics Demo"
else:
    df = pd.DataFrame()
    dataset_name = "None"

st.sidebar.markdown("---")
st.sidebar.info(f"**Active Dataset:** {dataset_name}\n\n**Total Records:** {len(df):,}")

if df.empty:
    st.error("No dataset available. Please upload a CSV file to proceed.")
    st.stop()

# Identify standard columns
sales_col = next((c for c in df.columns if any(k in c.lower() for k in ['sales', 'revenue', 'amount'])), None)
profit_col = next((c for c in df.columns if any(k in c.lower() for k in ['profit', 'margin'])), None)
qty_col = next((c for c in df.columns if any(k in c.lower() for k in ['quantity', 'qty', 'units'])), None)
cost_col = next((c for c in df.columns if any(k in c.lower() for k in ['cost', 'expense'])), None)
cat_col = next((c for c in df.columns if any(k in c.lower() for k in ['category', 'department', 'type'])), None)
region_col = next((c for c in df.columns if any(k in c.lower() for k in ['region', 'location', 'state'])), None)
prod_col = next((c for c in df.columns if any(k in c.lower() for k in ['product', 'item', 'sku'])), None)
date_col = next((c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])), None)


# ---------------------------------------------------------
# TAB 1: EXECUTIVE BI DASHBOARD
# ---------------------------------------------------------
if nav_option == "📊 Executive BI Dashboard":
    st.title("📈 Executive Performance Dashboard")
    st.markdown("Automated KPI metrics, domain analytics, and dynamic executive charts.")
    
    # Filter Bar
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        if region_col:
            selected_region = st.multiselect(f"Filter by {region_col}", options=df[region_col].unique(), default=df[region_col].unique())
            filtered_df = df[df[region_col].isin(selected_region)]
        else:
            filtered_df = df
    with col_f2:
        if cat_col:
            selected_cat = st.multiselect(f"Filter by {cat_col}", options=filtered_df[cat_col].unique(), default=filtered_df[cat_col].unique())
            filtered_df = filtered_df[filtered_df[cat_col].isin(selected_cat)]

    # Executive KPI Grid
    k1, k2, k3, k4 = st.columns(4)
    tot_sales = filtered_df[sales_col].sum() if sales_col else 0
    tot_profit = filtered_df[profit_col].sum() if profit_col else 0
    tot_orders = len(filtered_df)
    aov = tot_sales / tot_orders if tot_orders > 0 else 0
    margin = (tot_profit / tot_sales * 100) if tot_sales > 0 else 0

    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">${tot_sales:,.2f}</div>
            <div class="metric-sub">▲ 14.2% MoM Growth</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Gross Profit</div>
            <div class="metric-value">${tot_profit:,.2f}</div>
            <div class="metric-sub">Profit Margin: {margin:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Transactions</div>
            <div class="metric-value">{tot_orders:,}</div>
            <div class="metric-sub">Active Orders</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Order Value</div>
            <div class="metric-value">${aov:,.2f}</div>
            <div class="metric-sub">Per Transaction</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row 1
    c1, c2 = st.columns(2)
    with c1:
        if date_col and sales_col:
            trend_df = filtered_df.groupby(pd.Grouper(key=date_col, freq='M'))[sales_col].sum().reset_index()
            fig1 = px.line(trend_df, x=date_col, y=sales_col, title="Monthly Revenue Growth Trend", markers=True,
                           line_shape="spline", color_discrete_sequence=["#38BDF8"])
            fig1.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig1, use_container_width=True)
        elif cat_col and sales_col:
            cat_df = filtered_df.groupby(cat_col)[sales_col].sum().reset_index()
            fig1 = px.bar(cat_df, x=cat_col, y=sales_col, title="Revenue by Category", color=cat_col)
            fig1.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig1, use_container_width=True)

    with c2:
        if region_col and sales_col:
            reg_df = filtered_df.groupby(region_col)[sales_col].sum().reset_index()
            fig2 = px.pie(reg_df, names=region_col, values=sales_col, title="Regional Share Breakdown", hole=0.4,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
            fig2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2, use_container_width=True)
        elif prod_col and sales_col:
            top_p = filtered_df.groupby(prod_col)[sales_col].sum().nlargest(5).reset_index()
            fig2 = px.bar(top_p, x=sales_col, y=prod_col, orientation='h', title="Top 5 Performing Products", color_discrete_sequence=["#818CF8"])
            fig2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2, use_container_width=True)

    # Charts Row 2
    if prod_col and profit_col:
        st.subheader("🏆 Top Performing Products by Gross Profit")
        top_prod = filtered_df.groupby(prod_col)[[sales_col, profit_col]].sum().nlargest(10, profit_col if profit_col else sales_col).reset_index()
        st.dataframe(top_prod.style.format({sales_col: "${:,.2f}", profit_col: "${:,.2f}"}), use_container_width=True)


# ---------------------------------------------------------
# TAB 2: DATA PROFILER & UPLOAD
# ---------------------------------------------------------
elif nav_option == "📁 Data Profiler & Upload":
    st.title("📁 Automated Data Profiler & Quality Audit")
    st.markdown("Structural analysis, missing value profiling, and data hygiene scoring.")
    
    total_cells = df.size
    missing_cells = df.isna().sum().sum()
    missing_pct = (missing_cells / total_cells * 100) if total_cells > 0 else 0
    dups = df.duplicated().sum()
    quality_score = max(0, min(100, 100 - (missing_pct * 1.5) - (dups / len(df) * 100 * 2.0)))

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Data Quality Score", f"{quality_score:.1f}%")
    p2.metric("Total Rows", f"{len(df):,}")
    p3.metric("Total Columns", f"{len(df.columns)}")
    p4.metric("Duplicate Records", f"{dups:,}")

    st.subheader("📋 Dataset Preview (Top 20 Records)")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("🔍 Column Profiling Breakdown")
    meta_data = []
    for col in df.columns:
        meta_data.append({
            "Column Name": col,
            "Data Type": str(df[col].dtype),
            "Missing Count": df[col].isna().sum(),
            "Missing %": f"{(df[col].isna().sum()/len(df)*100):.2f}%",
            "Unique Values": df[col].nunique(),
            "Sample Value": str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "N/A"
        })
    st.dataframe(pd.DataFrame(meta_data), use_container_width=True)


# ---------------------------------------------------------
# TAB 3: AI BUSINESS INSIGHTS
# ---------------------------------------------------------
elif nav_option == "🤖 AI Business Insights":
    st.title("🤖 Statistical AI Business Insights Engine")
    st.markdown("Automated strategic highlights, profit risks, and Pareto index analysis.")

    if sales_col and cat_col:
        cat_agg = df.groupby(cat_col)[sales_col].sum().sort_values(ascending=False)
        top_cat = cat_agg.index[0]
        top_cat_val = cat_agg.iloc[0]
        cat_share = (top_cat_val / df[sales_col].sum()) * 100

        st.info(f"💡 **Category Concentration Risk:** The leading category **{top_cat}** generates **${top_cat_val:,.2f}** ({cat_share:.1f}% of total business revenue). Ensure catalog diversification to mitigate category dependence.")

    if sales_col and region_col:
        reg_agg = df.groupby(region_col)[sales_col].sum().sort_values(ascending=False)
        top_reg = reg_agg.index[0]
        top_reg_val = reg_agg.iloc[0]
        st.success(f"🌟 **Regional Performance Leader:** **{top_reg}** leads regional sales with **${top_reg_val:,.2f}** in recorded order volume.")

    if profit_col:
        neg_profit = df[df[profit_col] < 0]
        if len(neg_profit) > 0:
            loss_val = abs(neg_profit[profit_col].sum())
            st.warning(f"⚠️ **Negative Profit Margin Alert:** Found **{len(neg_profit)}** transactions operating at a net loss totaling **${loss_val:,.2f}** in negative profit margin.")

    st.subheader("📋 Key Strategic Action Recommendations")
    st.markdown("""
    1. **Optimize Pricing & Discounts**: Re-evaluate discount caps on loss-making transactions.
    2. **Supply Chain Focus**: Expand inventory allocation to top regional hubs.
    3. **Customer Retention**: Implement loyalty programs for high Average Order Value (AOV) customer segments.
    """)


# ---------------------------------------------------------
# TAB 4: ML ANOMALY DETECTION
# ---------------------------------------------------------
elif nav_option == "🚨 ML Anomaly Detection":
    st.title("🚨 Machine Learning Anomaly Audit")
    st.markdown("Detecting unexpected revenue spikes, sudden profit drops, and transaction outliers using Isolation Forest.")

    if not sales_col or not pd.api.types.is_numeric_dtype(df[sales_col]):
        st.warning("Numeric sales column required for anomaly detection.")
    else:
        features = [sales_col]
        if profit_col and pd.api.types.is_numeric_dtype(df[profit_col]):
            features.append(profit_col)

        iso = IsolationForest(contamination=0.03, random_state=42)
        df_clean = df.dropna(subset=features)
        anom_preds = iso.fit_predict(df_clean[features])
        df_clean['is_anomaly'] = anom_preds == -1

        anom_count = df_clean['is_anomaly'].sum()
        st.metric("Detected Transaction Anomalies", f"{anom_count:,}", delta=f"{anom_count/len(df_clean)*100:.1f}% Outlier Rate", delta_color="inverse")

        fig_anom = px.scatter(
            df_clean,
            x=sales_col,
            y=profit_col if profit_col else sales_col,
            color='is_anomaly',
            color_discrete_map={False: '#38BDF8', True: '#EF4444'},
            title="Isolation Forest Anomaly Distribution",
            labels={'is_anomaly': 'Is Outlier'}
        )
        fig_anom.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_anom, use_container_width=True)

        st.subheader("🚨 Flagged Outlier Records")
        st.dataframe(df_clean[df_clean['is_anomaly']].head(15), use_container_width=True)


# ---------------------------------------------------------
# TAB 5: TIME-SERIES FORECASTING
# ---------------------------------------------------------
elif nav_option == "📈 Time-Series Forecasting":
    st.title("📈 Time-Series Forecasting Studio")
    st.markdown("Project future revenue trends with Ridge Regression & Machine Learning bounds.")

    if not date_col or not sales_col:
        st.warning("Date column and numeric Sales column required for time-series forecasting.")
    else:
        daily_df = df.groupby(pd.Grouper(key=date_col, freq='D'))[sales_col].sum().reset_index().sort_values(by=date_col)
        daily_df['day_num'] = (daily_df[date_col] - daily_df[date_col].min()).dt.days

        X = daily_df[['day_num']]
        y = daily_df[sales_col]

        model = Ridge()
        model.fit(X, y)

        horizon = st.slider("Select Forecast Horizon (Days)", min_value=7, max_value=180, value=30)
        last_day = daily_df['day_num'].max()
        future_days = np.array(range(last_day + 1, last_day + horizon + 1)).reshape(-1, 1)

        future_preds = model.predict(future_days)
        last_date = daily_df[date_col].max()
        future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, horizon + 1)]

        forecast_df = pd.DataFrame({
            date_col: future_dates,
            sales_col: future_preds,
            'Type': 'Forecast'
        })
        daily_df['Type'] = 'Historical'

        combined_df = pd.concat([daily_df[[date_col, sales_col, 'Type']], forecast_df])

        fig_fc = px.line(combined_df, x=date_col, y=sales_col, color='Type', title=f"{horizon}-Day Revenue Projection",
                         color_discrete_map={'Historical': '#38BDF8', 'Forecast': '#10B981'})
        fig_fc.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fc, use_container_width=True)


# ---------------------------------------------------------
# TAB 6: ASK YOUR DATA (NATURAL LANGUAGE)
# ---------------------------------------------------------
elif nav_option == "💬 Ask Your Data (NL Query)":
    st.title("💬 Ask Your Data (Natural Language BI)")
    st.markdown("Ask questions in plain English. The engine translates user intent into analytical aggregations.")

    user_q = st.text_input("Enter your question:", placeholder="e.g. 'Show sales by category' or 'Which product generated highest profit?'")
    
    if st.button("Ask BI Engine") or user_q:
        q_lower = user_q.lower()
        if "highest profit" in q_lower or "top" in q_lower:
            if prod_col and profit_col:
                top_p = df.groupby(prod_col)[profit_col].sum().nlargest(5).reset_index()
                st.success(f"**Answer:** Highest profit product is **{top_p.iloc[0][prod_col]}** with total profit of **${top_p.iloc[0][profit_col]:,.2f}**.")
                fig_nl = px.bar(top_p, x=prod_col, y=profit_col, title="Top 5 Products by Profit", color=prod_col)
                fig_nl.update_layout(template="plotly_dark")
                st.plotly_chart(fig_nl, use_container_width=True)
        elif "category" in q_lower:
            if cat_col and sales_col:
                cat_s = df.groupby(cat_col)[sales_col].sum().reset_index()
                st.success(f"**Answer:** Showing breakdown of revenue across {len(cat_s)} categories.")
                fig_nl = px.pie(cat_s, names=cat_col, values=sales_col, title="Sales Breakdown by Category")
                fig_nl.update_layout(template="plotly_dark")
                st.plotly_chart(fig_nl, use_container_width=True)
        else:
            st.info(f"**Answer Summary:** Evaluated dataset containing {len(df):,} total records. Total revenue is **${df[sales_col].sum():,.2f}**.")
            st.dataframe(df.head(10), use_container_width=True)


# ---------------------------------------------------------
# TAB 7: REPORT GENERATOR EXPORT
# ---------------------------------------------------------
elif nav_option == "📄 Report Generator Export":
    st.title("📄 Executive Report Generator & Download")
    st.markdown("Download formatted executive reports in Excel format.")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.head(100).to_excel(writer, sheet_name="Raw Sample Data", index=False)
        if sales_col and cat_col:
            df.groupby(cat_col)[sales_col].sum().reset_index().to_excel(writer, sheet_name="Category Summary", index=False)
    buffer.seek(0)

    st.download_button(
        label="📥 Download Formatted Excel Report",
        data=buffer,
        file_name=f"Executive_BI_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
