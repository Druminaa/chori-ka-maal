# Vercel + Railway Deployment Guide

## Backend Deployment (Railway)

1. **Deploy to Railway:**
   ```bash
   # Push your backend code to GitHub
   git add backend/
   git commit -m "Backend ready for Railway"
   git push
   ```

2. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Select the repository
   - Railway will auto-detect the `railway.json` config

3. **Get Railway URL:**
   - After deployment, copy your Railway app URL
   - Format: `https://your-app-name.railway.app`

## Frontend Deployment (Vercel)

1. **Update Environment Variables:**
   - Replace `https://your-railway-app.railway.app` in:
     - `frontend/.env.production`
     - `vercel.json`
   - Use your actual Railway URL

2. **Deploy to Vercel:**
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Deploy
   vercel --prod
   ```

3. **Alternative - GitHub Integration:**
   - Connect your GitHub repo to Vercel
   - Set environment variable in Vercel dashboard:
     - `NEXT_PUBLIC_API_URL` = `https://your-railway-app.railway.app`

## Environment Variables Setup

### Railway (Backend)
No additional environment variables needed.

### Vercel (Frontend)
Set in Vercel dashboard or `vercel.json`:
- `NEXT_PUBLIC_API_URL` = Your Railway backend URL

## Testing the Connection

1. Deploy backend to Railway first
2. Update frontend with Railway URL
3. Deploy frontend to Vercel
4. Test the connection by fetching video info

## CORS Configuration

The backend is configured to accept requests from:
- `localhost:3000` (development)
- `*.vercel.app` (Vercel deployments)

## Troubleshooting

- **CORS errors**: Ensure Railway URL is correct in frontend env
- **Network errors**: Check Railway app is running
- **Build errors**: Verify all dependencies in `requirements.txt`