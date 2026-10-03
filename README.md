# AI-Powered Automated Business Intelligence (BI) Reporting Platform

A commercial-grade, full-stack Automated Business Intelligence SaaS platform designed to transform raw business data into actionable executive dashboards, AI strategic insights, statistical anomaly audits, time-series forecasting, automated PDF/Excel reports, and scheduled email delivery.

---

## Key Features

1. **JWT Authentication & Multi-Tenant Workspaces**:
   - Secure passlib/bcrypt password hashing.
   - User registration, login, profile management.
   - Role-Based Access Control (Admin, Analyst, Viewer) & workspace isolation.

2. **Data Upload & Structure Profiling**:
   - Accepts **CSV, XLSX, XLS, JSON** files up to 50MB.
   - Automated column profiling (Numeric, Categorical, Datetime, ID).
   - Instant **Data Quality Score (0-100%)** measuring missing values, duplicates, and type consistency.

3. **Intelligent Data Preprocessing Pipeline**:
   - Automated missing value imputation (median for numeric, mode for categorical).
   - Duplicate record purging.
   - ISO Date parsing and standardisation.
   - Outlier capping using 1.5x Interquartile Range (IQR).
   - Full **Transformation Audit Log** detailing every modification step.

4. **Automated Business Domain & Extensible KPI Engine**:
   - Automatically detects business domain (Sales, Retail, E-commerce, Finance, HR, Inventory, Marketing, Healthcare, Customer Analytics).
   - Dynamically computes domain KPIs: **Total Revenue, Total Orders, Average Order Value (AOV), Gross Profit, Profit Margin, Active Customer Count, Units Sold, Revenue Growth**.

5. **Automated BI Dashboard Generator**:
   - Generates interactive, customizable visual dashboard specs automatically.
   - Rich Chart visualizers: Executive KPI Cards, Multi-line Trend Charts, Performance Bar Charts, Regional Donut Charts, Category Area Charts, Top-N Products Tables.
   - Dynamic dynamic filtering by Date Range, Region, Category, Customer Segment.

6. **AI Business Insights Engine**:
   - Ground-truth statistical analysis calculating MoM growth, regional share, margin concentration risks, and product Pareto index.
   - Configurable LLM API layer (OpenAI) with smart fallback rule-engine.

7. **Machine Learning Anomaly Detection**:
   - Detects sudden revenue drops, order spikes, or profit anomalies using **Z-score thresholding** and **Isolation Forest**.
   - Interactive anomaly audit timeline with severity indicators (Critical, High, Medium, Low).

8. **Time-Series Forecasting Studio**:
   - Models: **Linear Trend Model, Ridge Regression, Random Forest Regressor**.
   - Horizon options: **7 Days, 30 Days, 90 Days, 180 Days**.
   - Interactive timeline visualization with projected upper/lower 95% confidence bounds and R², RMSE, MAE model metrics.

9. **"Ask Your Data" Natural Language BI**:
   - Plain-English natural language query processor.
   - Translates text intent into safe, structured Pandas aggregations (e.g., *"Show me sales for West region"*, *"Which product generated the highest profit?"*).
   - Returns text summary, generated chart preview, filtered data table, and executing code string.

10. **Automated Executive PDF & Excel Report Generator**:
    - **Executive PDF Builder**: Formatted executive report generated via ReportLab featuring brand header, KPI summary grid, AI insights, and anomaly logs.
    - **Excel Builder**: Formatted multi-tab workbook generated via OpenPyXL containing Executive Summary, Raw Data, and Data Quality Audit.

11. **Scheduled Report Job Automation & Emailer**:
    - Background scheduler powered by **APScheduler** supporting Daily, Weekly, and Monthly recurring jobs.
    - Automated SMTP email dispatch delivering PDF/Excel attachments directly to configured distribution lists.

---

## Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pandas, NumPy, Scikit-Learn, ReportLab, OpenPyXL, APScheduler, PyJWT, Passlib, Pytest.
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons, Axios.
- **Database**: SQLite (default zero-config local run) / PostgreSQL native support.
- **Infrastructure**: Docker, Docker Compose, Nginx.

---

## Getting Started

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ & npm

### 2. Local Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run backend server
python -m uvicorn app.main:app --reload --port 8000
```
Backend API interactive documentation available at: `http://localhost:8000/docs`

### 3. Local Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Access the application at: `http://localhost:3000`

### 4. Running Backend Test Suite
```bash
# Run pytest verification suite
$env:PYTHONPATH="backend"; python -m pytest backend/tests
```

---

## Docker Deployment

To launch the full production environment (Backend, Frontend, PostgreSQL, Redis) using Docker Compose:

```bash
docker-compose up --build
```
- Frontend UI: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

---

## Demo Dataset

The repository includes a realistic **Retail Sales Analytics** dataset (`data/retail_sales_demo.csv`) pre-seeded with 1,200+ transaction records spanning 2024-2026 across regions, categories, products, customer segments, sales, costs, profits, discounts, and order dates.
