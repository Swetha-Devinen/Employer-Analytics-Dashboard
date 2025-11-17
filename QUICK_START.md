# 🚀 Quick Start Guide - Web Dashboard

## Get Your Dashboard Running in 5 Minutes!

### Step 1: Install Dependencies

**Backend (Python):**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend (Node.js):**
```bash
cd frontend
npm install
```

### Step 2: Generate Predictions (if needed)

```bash
cd python
python train_and_predict.py
```

This creates `data/sample_predictions.csv` with AI predictions.

### Step 3: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```
✅ Backend running on http://localhost:5000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
✅ Frontend running on http://localhost:3000

### Step 4: Open Dashboard

Open your browser to: **http://localhost:3000**

🎉 Your dashboard is now running!

## 📊 What You'll See

- **Home Page**: Overview with KPIs and key metrics
- **Salary Overview**: Market salary insights by role and location
- **Predictions**: AI predictions with accuracy analysis
- **Benchmarking**: Employer vs Market comparison
- **Compensation Types**: Hourly vs Yearly analysis

## 🎯 Features

✅ AI-Powered Salary Predictions  
✅ Interactive Charts & Visualizations  
✅ Real-time Filtering  
✅ Benchmarking Analysis  
✅ Responsive Design  

## 🐛 Troubleshooting

**Backend won't start?**
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r backend/requirements.txt`
- Check data files exist in `data/` folder

**Frontend won't start?**
- Check Node version: `node --version` (need 16+)
- Install dependencies: `npm install` in frontend folder
- Clear cache: `rm -rf node_modules package-lock.json && npm install`

**No data showing?**
- Ensure CSV files are in `data/` folder
- Check backend is running on port 5000
- Check browser console for errors

---

**Ready to explore?** Start both servers and open http://localhost:3000! 🚀


