# 🚀 Deployment Guide

## Vercel Deployment (Frontend)

### Option 1: Vercel CLI
```bash
cd frontend
npm install -g vercel
vercel
```

### Option 2: Vercel Dashboard
1. Go to https://vercel.com
2. Import your GitHub repository
3. **Root Directory**: Set to `frontend`
4. **Framework Preset**: Next.js
5. **Build Command**: `npm run build`
6. **Output Directory**: `.next`
7. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL` = Your backend URL

### Fix 404 Error
If you see 404 after deployment:
1. Check Vercel project settings
2. Set **Root Directory** to `frontend`
3. Redeploy

## Backend Deployment Options

### Option 1: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
cd backend
railway login
railway init
railway up
```

### Option 2: Render
1. Go to https://render.com
2. New Web Service
3. Connect GitHub repo
4. **Root Directory**: `backend`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

### Option 3: Heroku
```bash
cd backend
heroku create your-app-name
git push heroku main
```

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend
No environment variables needed for basic setup.

## Common Issues

### 404 Error
- Ensure root directory is set to `frontend` in Vercel
- Check that `page.tsx` exists in `app/` folder
- Verify build completed successfully

### CORS Error
- Update backend API URL in frontend `.env.local`
- Backend already configured for CORS

### Build Failed
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run build
```

## Quick Deploy Commands

```bash
# Frontend to Vercel
cd frontend
vercel --prod

# Backend to Railway
cd backend
railway up

# Update environment
cd frontend
echo "NEXT_PUBLIC_API_URL=https://your-backend.railway.app" > .env.local
vercel --prod
```
