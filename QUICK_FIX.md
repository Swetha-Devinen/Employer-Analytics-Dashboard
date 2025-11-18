# 🚨 Quick Fix - Dashboard Not Showing Data

## The Problem
Your dashboard was working yesterday but now graphs and data aren't showing.

## ✅ What I Found
- **Backend:** ✅ Running and working correctly
- **All API Endpoints:** ✅ Responding with data
- **Data Files:** ✅ Present and correct
- **Frontend:** ❓ May not be running

## 🔧 Solution

### Step 1: Check What's Running

**Run this command:**
```bash
check_status.bat
```

Or manually check:

**Backend Check:**
Open browser: http://localhost:5000/api/health
- Should show: `{"status": "healthy", "data_loaded": true}`

**Frontend Check:**
Open browser: http://localhost:3000
- Should show the dashboard
- If blank or error, frontend not running

### Step 2: Start Frontend (If Not Running)

**Open a new terminal and run:**
```bash
cd frontend
npm run dev
```

**You should see:**
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:3000/
```

### Step 3: Check Browser Console

1. Open http://localhost:3000
2. Press **F12** (Developer Tools)
3. Click **Console** tab
4. Look for errors (red text)

**Common errors you might see:**

**"Failed to fetch" or "Network Error"**
- Backend not running → Start backend
- Wrong URL → Check API_BASE_URL in frontend/src/api/api.js

**"Cannot read property of undefined"**
- Data not loaded → Check Network tab for API calls
- API returning error → Check backend console

### Step 4: Check Network Tab

1. Press **F12** → **Network** tab
2. Refresh page (**F5**)
3. Look for these API calls:
   - `/api/analytics/overview-kpis` → Should be **200** (green)
   - `/api/analytics/salary-by-role` → Should be **200** (green)
   - `/api/analytics/top-skills` → Should be **200** (green)
   - `/api/analytics/salary-trends` → Should be **200** (green)

**If any show red (error):**
- Click on it to see error details
- Check backend console for errors

## 🎯 Most Likely Issue

**Frontend server stopped running**

**Why this happens:**
- Terminal was closed
- Computer was restarted
- Server crashed

**Fix:**
```bash
cd frontend
npm run dev
```

## ✅ Verification

After starting frontend:

1. **Open:** http://localhost:3000
2. **You should see:**
   - 4 KPI cards at the top
   - 3 charts below
   - No "Loading..." message

3. **If still not working:**
   - Check browser console (F12)
   - Check Network tab
   - Check backend terminal for errors

## 🚀 Quick Start (Both Servers)

**Terminal 1:**
```bash
cd backend
python app.py
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

**Then open:** http://localhost:3000

## 📞 Still Not Working?

1. **Check backend is running:**
   - Open: http://localhost:5000/api/health
   - Should return JSON

2. **Check frontend is running:**
   - Open: http://localhost:3000
   - Should show dashboard (even if no data)

3. **Check browser console:**
   - F12 → Console tab
   - Look for errors

4. **Restart everything:**
   - Stop both servers (Ctrl+C in terminals)
   - Start backend again
   - Start frontend again
   - Clear browser cache (Ctrl+Shift+Delete)

---

**The backend is working fine. The issue is likely the frontend server not running.**

