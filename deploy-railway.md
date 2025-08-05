# Quick Railway Deployment Guide

Railway is the easiest way to deploy your full-stack application for free!

## 🚀 Why Railway?

- **All-in-one**: Deploy frontend, backend, and database
- **Free**: $5 credit monthly (enough for small projects)
- **Simple**: Connect GitHub and deploy automatically
- **Fast**: Deploy in minutes, not hours

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be on GitHub
2. **Railway Account**: Sign up at https://railway.app
3. **5 minutes**: That's all you need!

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Run the deployment script**:
   ```bash
   # On Windows
   deploy.bat
   
   # On Mac/Linux
   ./deploy.sh
   ```

2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

### Step 2: Deploy to Railway

1. **Go to Railway**: https://railway.app
2. **Sign up** with your GitHub account
3. **Create New Project** → "Deploy from GitHub repo"
4. **Select your repository**
5. **Railway will automatically detect your services**

### Step 3: Add Services

Railway will create services for you:

1. **Backend Service** (Python/FastAPI)
   - Framework: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Frontend Service** (Node.js/React)
   - Framework: Node.js
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **PostgreSQL Database**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will create it automatically

### Step 4: Configure Environment Variables

**Backend Service Variables**:
```bash
DATABASE_URL=postgresql://... (Railway will set this automatically)
SECRET_KEY=your_super_secret_key_here
ENVIRONMENT=production
DEBUG=false
```

**Frontend Service Variables**:
```bash
VITE_API_URL=https://your-backend-service-url.railway.app/api/v1
```

### Step 5: Deploy

1. **Railway will deploy automatically**
2. **Wait for build to complete** (2-5 minutes)
3. **Your app is live!**

## 🔗 Your URLs

After deployment, you'll get:

- **Frontend**: `https://your-frontend-service.railway.app`
- **Backend API**: `https://your-backend-service.railway.app`
- **API Docs**: `https://your-backend-service.railway.app/docs`
- **Health Check**: `https://your-backend-service.railway.app/health`

## 🧪 Test Your Deployment

1. **Visit your frontend URL**
2. **Try to login** (create a test user first)
3. **Create a project**
4. **Add some tasks**
5. **Check everything works**

## 🔧 Custom Domain (Optional)

1. **Go to your service settings**
2. **Click "Domains"**
3. **Add your custom domain**
4. **Update DNS records**

## 📊 Monitor Your App

Railway provides:
- **Real-time logs**
- **Performance metrics**
- **Deployment history**
- **Error tracking**

## 🆘 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Railway logs
   - Verify all dependencies are in requirements.txt/package.json

2. **Database Connection Error**
   - Check DATABASE_URL environment variable
   - Ensure PostgreSQL service is running

3. **Frontend Can't Connect to Backend**
   - Verify VITE_API_URL is correct
   - Check CORS settings

### Get Help

- **Railway Discord**: https://discord.gg/railway
- **Railway Docs**: https://docs.railway.app
- **Community**: https://community.railway.app

## 💰 Cost Management

- **Free Tier**: $5 credit monthly
- **Typical Usage**: ~$2-3/month for small projects
- **Upgrade**: Only when you need more resources

## 🎉 You're Done!

Your Project Management Dashboard is now live on the internet for free!

**Next Steps**:
1. Share your app URL with friends
2. Add more features
3. Monitor usage and performance
4. Consider upgrading when you need more resources

## 🔄 Updates

To update your app:
1. Push changes to GitHub
2. Railway deploys automatically
3. Your app updates in minutes

That's it! Railway makes deployment super simple! 🚀 