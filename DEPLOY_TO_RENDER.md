# Deploy Backend to Render - Step by Step Guide

## Prerequisites
- GitHub account
- Render account (free at https://render.com)
- Your code pushed to GitHub

## Step 1: Push Code to GitHub

Make sure all your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Add Render configuration files"
git push origin main
```

## Step 2: Sign Up / Login to Render

1. Go to https://render.com
2. Sign up with your GitHub account (or login if you already have an account)
3. Authorize Render to access your GitHub repositories

## Step 3: Create New Web Service

1. Click **"New +"** button in the top right
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - If not connected, click "Connect GitHub" and authorize
   - Search for your repository: `dashboard` (or your repo name)
   - Click **"Connect"**

## Step 4: Configure the Service

Render should automatically detect the `render.yaml` file. If it does:

1. **Name**: `dashboard-backend` (or any name you prefer)
2. **Region**: Choose closest to you (Oregon is default)
3. **Branch**: `main` (or your main branch)
4. **Root Directory**: Leave empty (or set to `backend` if auto-detection doesn't work)
5. **Runtime**: Python 3
6. **Build Command**: `pip install -r backend/requirements.txt`
7. **Start Command**: `cd backend && python app.py`

**OR** if Render detected `render.yaml`:
- Just review the settings and click **"Create Web Service"**

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying
3. Wait 5-10 minutes for the first deployment
4. You'll see build logs in real-time

## Step 6: Get Your Backend URL

Once deployed, you'll see:
- **Service URL**: `https://dashboard-backend-xxxx.onrender.com`
- Copy this URL - you'll need it for the frontend!

## Step 7: Test Your Backend

1. Visit: `https://your-backend-url.onrender.com/api/health`
2. You should see: `{"status": "healthy", "data_loaded": true, ...}`

## Step 8: Update Frontend API URL

1. Go to your Vercel project settings
2. Add environment variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.onrender.com/api`
3. Redeploy your frontend on Vercel

## Step 9: Keep Backend Awake (Free)

To prevent the 15-minute sleep:

1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add New Monitor:
   - **Type**: HTTP(s)
   - **URL**: `https://your-backend-url.onrender.com/api/health`
   - **Interval**: 5 minutes
4. Save

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Check Python version compatibility

### Backend Not Starting
- Check start command: `cd backend && python app.py`
- Verify `app.py` exists in `backend/` folder
- Check logs in Render dashboard

### CORS Errors
- Backend already has `CORS(app)` configured
- If issues persist, check frontend URL is allowed

### Data Not Loading
- Verify CSV files are in `data/` folder
- Check file paths in `app.py` are correct
- Review logs for file loading errors

## Important Notes

- **Free Tier**: Backend sleeps after 15 minutes of inactivity
- **Cold Start**: First request after sleep takes 30-60 seconds
- **Solution**: Use UptimeRobot (free) to ping every 5 minutes
- **Upgrade**: $7/month for always-on service (optional)

## Next Steps

1. ✅ Deploy backend on Render
2. ✅ Get backend URL
3. ✅ Update frontend API URL in Vercel
4. ✅ Set up UptimeRobot to keep backend awake
5. ✅ Test the full application!

## Support

If you encounter issues:
- Check Render logs: Dashboard → Your Service → Logs
- Check build logs for errors
- Verify all file paths are correct
- Ensure all dependencies are in `requirements.txt`

