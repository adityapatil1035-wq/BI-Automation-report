# 🚀 Deployment Guide: Streamlit Cloud & GitHub

This repository contains a full-featured Streamlit BI platform (`app_streamlit.py`), FastAPI backend (`backend/`), and React Vite frontend (`frontend/`).

---

## 🌟 Option 1: Deploy to Streamlit Community Cloud (Recommended & Free)

Streamlit Cloud hosts Python Streamlit applications for free directly from GitHub.

### Step 1: Push Repository to GitHub
If you haven't pushed your code to GitHub yet, follow **Option 2** below.

### Step 2: Deploy on Streamlit Cloud
1. Navigate to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **"New App"**.
3. Fill in the repository details:
   - **Repository:** `YOUR_GITHUB_USERNAME/BI-Report-Automation`
   - **Branch:** `main`
   - **Main file path:** `app_streamlit.py`
4. Click **Deploy!**
5. Your application will be live at a public URL (e.g. `https://bi-report-automation.streamlit.app`) in under 60 seconds!

---

## 🐙 Option 2: Upload Project to GitHub

### Method A: Using Git CLI (PowerShell / Command Prompt)

1. Download and install **[Git for Windows](https://git-scm.com/download/win)**.
2. Open PowerShell in your project directory `c:\Users\aadir\OneDrive\Desktop\BI Report Automation`.
3. Initialize git and make your first commit:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit - AI-Powered Automated BI Reporting Platform"
   ```
4. Create a new repository on **[github.com/new](https://github.com/new)** named `BI-Report-Automation`.
5. Connect your local repository and push:
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/BI-Report-Automation.git
   git branch -M main
   git push -u origin main
   ```

---

## 💻 Option 3: Local Launch Commands

### 1. Run Streamlit BI App
```powershell
python -m streamlit run app_streamlit.py
```
- **Local URL:** `http://localhost:8501`

### 2. Run Full-Stack FastAPI + React App
- **Backend API:**
  ```powershell
  cd backend
  python -m uvicorn app.main:app --reload --port 8000
  ```
- **Frontend App:**
  ```powershell
  cd frontend
  npm run dev
  ```
