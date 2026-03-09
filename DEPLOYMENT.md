# 🚀 Deployment Guide

## Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend) - RECOMMENDED

#### Step 1: Deploy Backend on Render

1. **Create Render Account**: Go to [render.com](https://render.com) and sign up
2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `backend` folder
3. **Configure Service**:
   - Name: `youtube-downloader-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables** (if needed):
   - None required for basic setup
5. **Deploy**: Click "Create Web Service"
6. **Copy URL**: Save your backend URL (e.g., `https://youtube-downloader-api.onrender.com`)

#### Step 2: Deploy Frontend on Vercel

1. **Create Vercel Account**: Go to [vercel.com](https://vercel.com) and sign up
2. **Import Project**:
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select the `frontend` folder as root directory
3. **Configure Project**:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
4. **Add Environment Variable**:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: Your Render backend URL (from Step 1)
5. **Deploy**: Click "Deploy"
6. **Update Backend URL**: Edit `frontend/vercel.json` and replace `your-backend-url.com` with your actual Render URL

---

### Option 2: Railway (Full Stack)

1. **Create Railway Account**: Go to [railway.app](https://railway.app)
2. **Deploy Backend**:
   - New Project → Deploy from GitHub
   - Select repository → Choose `backend` folder
   - Railway auto-detects Python
   - Add start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
3. **Deploy Frontend**:
   - Add service → Deploy from GitHub
   - Select repository → Choose `frontend` folder
   - Add environment variable: `NEXT_PUBLIC_API_URL` = backend URL
4. **Generate Domain**: Railway provides public URLs for both services

---

### Option 3: AWS EC2

1. **Launch EC2 Instance**:
   - Ubuntu 22.04 LTS
   - t2.medium or larger
   - Open ports: 22, 80, 443, 3000, 8000

2. **Connect and setup**:
```bash
ssh -i your-key.pem ubuntu@ec2-ip
sudo apt update && sudo apt upgrade -y
```

3. **Install dependencies**:
```bash
# Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Python
sudo apt install -y python3-pip python3-venv ffmpeg

# PM2 for process management
sudo npm install -g pm2
```

4. **Clone and setup**:
```bash
git clone <your-repo-url>
cd chori\ ka\ maal

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pm2 start "uvicorn api:app --host 0.0.0.0 --port 8000" --name backend

# Frontend
cd ../frontend
npm install
npm run build
pm2 start "npm start" --name frontend

# Save PM2 config
pm2 save
pm2 startup
```

---

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend (if needed)
```
PORT=8000
```

---

## Post-Deployment Checklist

- [ ] Backend is accessible at `/api/video-info`
- [ ] Frontend loads correctly
- [ ] CORS is configured properly
- [ ] SSL certificate is installed (for production)
- [ ] Environment variables are set
- [ ] Test video download functionality
- [ ] Monitor logs for errors

---

## Troubleshooting

### CORS Issues
Update `backend/api.py`:
```python
allow_origins=["https://your-frontend-domain.com"]
```

### Port Issues
Ensure ports 3000 and 8000 are open in firewall:
```bash
sudo ufw allow 3000
sudo ufw allow 8000
```

### FFmpeg Missing
```bash
sudo apt install ffmpeg -y
```

---

## Monitoring

### Check logs (PM2)
```bash
pm2 logs
```

### Restart services
```bash
pm2 restart all
```

---

## Cost Estimates

- **Vercel + Render**: Free tier available, ~$0-7/month
- **Railway**: ~$5-10/month
- **VPS (DigitalOcean)**: ~$6-12/month
- **AWS EC2**: ~$10-20/month

---

## Recommended: Vercel + Render (Free Tier)

This is the easiest and most cost-effective option for beginners:
1. Deploy backend on Render (free tier)
2. Deploy frontend on Vercel (free tier)
3. No server management required
4. Automatic SSL certificates
5. Easy to scale later
