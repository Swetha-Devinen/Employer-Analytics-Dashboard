# 🔧 Troubleshooting Guide

## Issue: Dashboard Not Showing Data/Graphs

### ✅ Current Status Check

**Backend Status:** ✅ RUNNING
- Server: http://localhost:5000
- Health Check: Working
- All API Endpoints: Working

**Data Files:** ✅ PRESENT
- sample_job_postings.csv: ✅
- sample_skills.csv: ✅
- sample_predictions.csv: ✅
- sample_employer_offers.csv: ✅

**API Endpoints Tested:** ✅ ALL WORKING
- /api/analytics/overview-kpis: ✅
- /api/analytics/salary-by-role: ✅
- /api/analytics/top-skills: ✅
- /api/analytics/salary-trends: ✅

---

## 🔍 How to Fix

### Step 1: Make Sure Backend is Running

**Check if backend is running:**
```bash
# Open browser or PowerShell
curl http://localhost:5000/api/health
```

**If not running, start it:**
```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
Data loaded successfully
```

### Step 2: Make Sure Frontend is Running

**Check if frontend is running:**
- Open browser to http://localhost:3000
- If page doesn't load, frontend is not running

**Start frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

### Step 3: Check Browser Console

1. Open browser (Chrome/Firefox/Edge)
2. Go to http://localhost:3000
3. Press F12 to open Developer Tools
4. Click "Console" tab
5. Look for errors (red text)

**Common Errors:**

**Error: "Network Error" or "Failed to fetch"**
- **Cause:** Backend not running or wrong URL
- **Fix:** Make sure backend is running on port 5000

**Error: "CORS policy"**
- **Cause:** Backend CORS not configured
- **Fix:** Backend already has CORS enabled, this shouldn't happen

**Error: "Cannot read property of undefined"**
- **Cause:** Data not loaded yet
- **Fix:** Check if API is returning data

### Step 4: Check Network Tab

1. Open Developer Tools (F12)
2. Click "Network" tab
3. Refresh page (F5)
4. Look for API calls:
   - `/api/analytics/overview-kpis`
   - `/api/analytics/salary-by-role`
   - `/api/analytics/top-skills`
   - `/api/analytics/salary-trends`

**Check each request:**
- Status should be 200 (green)
- Response should have data
- If status is 500, check backend console for errors

### Step 5: Verify Data Files

**Check if data files exist:**
```bash
# In PowerShell
dir data\*.csv
```

Should show:
- sample_job_postings.csv
- sample_skills.csv
- sample_predictions.csv
- sample_employer_offers.csv

**If files are missing, regenerate:**
```bash
python scripts/create_sample_data.py
```

---

## 🚀 Quick Fix Commands

### Start Everything Fresh

**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

**Then:**
- Open browser to http://localhost:3000
- Check console for errors
- Check Network tab for API calls

### Use Startup Script (Windows)

Double-click: `start_dashboard.bat`

This starts both servers automatically.

---

## 🔍 Common Issues & Solutions

### Issue 1: "Loading dashboard..." Forever

**Cause:** API calls failing
**Solution:**
1. Check backend is running
2. Check browser console for errors
3. Check Network tab for failed requests

### Issue 2: Charts Not Showing

**Cause:** Data not loading or wrong format
**Solution:**
1. Check API responses in Network tab
2. Verify data format matches what charts expect
3. Check browser console for chart errors

### Issue 3: Empty Charts

**Cause:** No data returned from API
**Solution:**
1. Check backend console for errors
2. Verify CSV files have data
3. Test API endpoint directly in browser

### Issue 4: CORS Errors

**Cause:** Backend CORS not working
**Solution:**
- Backend already has `CORS(app)` configured
- If still getting errors, restart backend

### Issue 5: Port Already in Use

**Error:** "Address already in use"

**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in backend/app.py (last line)
app.run(debug=True, port=5001)  # Change to different port
```

---

## ✅ Verification Checklist

- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 3000
- [ ] Data files exist in `data/` folder
- [ ] Backend health check returns: `{"status": "healthy"}`
- [ ] Browser console has no errors
- [ ] Network tab shows API calls with status 200
- [ ] API responses contain data

---

## 🆘 Still Not Working?

1. **Check Backend Logs:**
   - Look at terminal where backend is running
   - Check for error messages

2. **Check Frontend Logs:**
   - Look at terminal where frontend is running
   - Check for error messages

3. **Check Browser Console:**
   - F12 → Console tab
   - Look for red error messages

4. **Test API Directly:**
   - Open: http://localhost:5000/api/health
   - Should return JSON
   - If not, backend not running

5. **Restart Everything:**
   - Stop both servers (Ctrl+C)
   - Restart backend
   - Restart frontend
   - Clear browser cache (Ctrl+Shift+Delete)

---

## 📞 Quick Test

**Test Backend:**
```bash
curl http://localhost:5000/api/health
```

**Test Frontend:**
- Open: http://localhost:3000
- Should see dashboard

**Test API Endpoint:**
- Open: http://localhost:5000/api/analytics/overview-kpis
- Should see JSON data

If all three work, everything is fine!

