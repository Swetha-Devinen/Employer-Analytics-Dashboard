# 🚀 Running the Dashboard Locally

## Quick Start (Easiest Method)

### Option 1: Use the Startup Script (Windows)

Double-click **`start_dashboard.bat`** - This will start both servers automatically!

Or run from command line:
```bash
start_dashboard.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```
✅ Backend runs on http://localhost:5000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
✅ Frontend runs on http://localhost:3000

### Option 3: Individual Scripts

- **`start_backend.bat`** - Start only backend
- **`start_frontend.bat`** - Start only frontend

## 📋 Prerequisites Check

✅ **Data Files Created** - Sample data is in `data/` folder
✅ **Backend Dependencies** - Flask, pandas, etc. installed
✅ **Frontend Dependencies** - React, Recharts, etc. installed

## 🌐 Access the Dashboard

Once both servers are running:

**Open your browser to:** http://localhost:3000

## ✅ Verify It's Working

1. **Backend Health Check:**
   - Open: http://localhost:5000/api/health
   - Should return: `{"status":"healthy","data_loaded":true}`

2. **Frontend:**
   - Should show the dashboard homepage with KPIs and charts

## 🎯 Dashboard Pages

- **Home** - Overview with KPIs
- **Salary Overview** - Market insights
- **Predictions** - AI predictions
- **Benchmarking** - Employer vs Market
- **Compensation Types** - Hourly vs Yearly

## 🐛 Troubleshooting

**Backend won't start?**
- Check Python is installed: `python --version`
- Install dependencies: `pip install flask flask-cors pandas numpy scikit-learn`
- Check port 5000 is not in use

**Frontend won't start?**
- Check Node.js is installed: `node --version`
- Install dependencies: `cd frontend && npm install`
- Check port 3000 is not in use

**No data showing?**
- Verify data files exist in `data/` folder:
  - `sample_job_postings.csv`
  - `sample_skills.csv`
  - `sample_predictions.csv`
  - `sample_employer_offers.csv`
- Check backend is running and accessible
- Check browser console for errors

**Port already in use?**
- Backend: Change port in `backend/app.py` (line 430)
- Frontend: Change port in `frontend/vite.config.js`

## 📊 What You'll See

- **4 KPI Cards**: Market Median, Predicted Salary, Accuracy, Total Postings
- **Interactive Charts**: Bar charts, line charts, pie charts, scatter plots
- **Filtering**: Filter by role, location, compensation type
- **Real-time Data**: All data loaded from backend API

## 🎉 You're All Set!

The dashboard is now running locally. Explore the different pages and features!

---

**Need help?** Check the browser console (F12) for any errors.



