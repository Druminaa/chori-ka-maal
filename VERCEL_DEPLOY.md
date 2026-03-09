# 🚀 Deploy Frontend to Vercel - Step by Step

## Prerequisites
- GitHub account
- Vercel account (free) - Sign up at [vercel.com](https://vercel.com)

---

## Step 1: Push Code to GitHub

1. **Initialize Git** (if not already done):
```bash
cd "chori ka maal"
git init
git add .
git commit -m "Initial commit"
```

2. **Create GitHub Repository**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name: `youtube-downloader`
   - Click "Create repository"

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/youtube-downloader.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend First (Important!)

Before deploying frontend, deploy your backend on Render:

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `youtube-downloader-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. **COPY YOUR BACKEND URL** (e.g., `https://youtube-downloader-api.onrender.com`)

---

## Step 3: Deploy Frontend to Vercel

### Method 1: Using Vercel Dashboard (Easiest)

1. **Go to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Click "Sign Up" and login with GitHub

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Select your `youtube-downloader` repository
   - Click "Import"

3. **Configure Project**:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: Click "Edit" → Select `frontend`
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)

4. **Add Environment Variable**:
   - Click "Environment Variables"
   - Add:
     - **Name**: `NEXT_PUBLIC_API_URL`
     - **Value**: Your Render backend URL (from Step 2)
     - Example: `https://youtube-downloader-api.onrender.com`

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your site will be live at `https://your-project.vercel.app`

---

### Method 2: Using Vercel CLI

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Login**:
```bash
vercel login
```

3. **Deploy**:
```bash
cd frontend
vercel
```

4. **Follow prompts**:
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N`
   - Project name? `youtube-downloader`
   - Directory? `./`
   - Override settings? `N`

5. **Add Environment Variable**:
```bash
vercel env add NEXT_PUBLIC_API_URL
```
Enter your backend URL when prompted.

6. **Deploy to Production**:
```bash
vercel --prod
```

---

## Step 4: Update Backend CORS

After deployment, update your backend to allow your Vercel domain:

Edit `backend/api.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-project.vercel.app"  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Push changes and Render will auto-deploy.

---

## Step 5: Test Your Deployment

1. Visit your Vercel URL
2. Paste a YouTube URL
3. Click "Fetch Video Info"
4. Select quality and download

---

## Troubleshooting

### Issue: API calls failing
**Solution**: Check environment variable
```bash
vercel env ls
```
Make sure `NEXT_PUBLIC_API_URL` is set correctly.

### Issue: CORS errors
**Solution**: Update backend CORS settings (see Step 4)

### Issue: Build fails
**Solution**: Check build logs in Vercel dashboard
- Usually missing dependencies
- Run `npm install` locally first

### Issue: Backend sleeping (Render free tier)
**Solution**: 
- Free tier sleeps after 15 min inactivity
- First request takes 30-60 seconds to wake up
- Upgrade to paid tier ($7/mo) for always-on

---

## Custom Domain (Optional)

1. In Vercel Dashboard → Settings → Domains
2. Add your domain
3. Update DNS records as shown
4. SSL certificate auto-generated

---

## Automatic Deployments

Every push to `main` branch automatically deploys to Vercel!

```bash
git add .
git commit -m "Update feature"
git push
```

Vercel will automatically build and deploy.

---

## Environment Variables Reference

### Frontend (.env.local for local dev)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Frontend (Vercel production)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

---

## Quick Commands

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# Remove deployment
vercel remove
```

---

## Cost

- **Vercel**: FREE (Hobby plan)
  - Unlimited deployments
  - Automatic SSL
  - 100GB bandwidth/month

- **Render Backend**: FREE
  - 750 hours/month
  - Sleeps after 15 min inactivity
  - 512MB RAM

**Total Cost: $0/month** 🎉

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Update CORS settings
4. ✅ Test the application
5. 🎉 Share your live URL!

---

## Support

If you encounter issues:
1. Check Vercel build logs
2. Check Render logs
3. Verify environment variables
4. Test API endpoint directly: `https://your-backend.onrender.com/api/video-info`
