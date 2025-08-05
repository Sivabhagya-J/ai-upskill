# Render Deployment Steps (After Sign In)

Now that you're signed in to Render, follow these steps to deploy your Project Management Dashboard.

## 🚀 Step 1: Create New Web Service

1. **Click "New"** in the top right corner
2. **Select "Web Service"**
3. **Connect your GitHub repository**:
   - Click "Connect account" if not already connected
   - Select your project repository
   - Click "Connect"

## 🎯 Step 2: Configure Backend Service

### Basic Settings
- **Name**: `project-management-backend` (or any name you prefer)
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: `backend` (important!)

### Build & Deploy Settings
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment Variables
Click "Advanced" and add these environment variables:

```bash
# Required
DATABASE_URL=postgresql://... (we'll set this after creating database)
SECRET_KEY=your_super_secret_key_here_make_it_long_and_random
ENVIRONMENT=production
DEBUG=false

# Optional
API_V1_STR=/api/v1
PROJECT_NAME=Project Management Dashboard
VERSION=1.0.0
```

## 🗄️ Step 3: Create PostgreSQL Database

1. **Go back to Dashboard**
2. **Click "New" → "PostgreSQL"**
3. **Configure Database**:
   - **Name**: `project-management-db`
   - **Region**: Same as your web service
   - **PostgreSQL Version**: Latest (14 or 15)
   - **Plan**: Free (90 days trial)

4. **Get Database URL**:
   - Click on your database
   - Go to "Connections" tab
   - Copy the "External Database URL"

5. **Update Backend Environment Variables**:
   - Go back to your web service
   - Click "Environment"
   - Update `DATABASE_URL` with the copied URL

## 🎨 Step 4: Create Frontend Service (Optional)

If you want to deploy frontend on Render too:

1. **Click "New" → "Static Site"**
2. **Connect same GitHub repository**
3. **Configure**:
   - **Name**: `project-management-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Publish Directory**: `dist`

4. **Add Environment Variables**:
```bash
VITE_API_URL=https://your-backend-service-url.onrender.com/api/v1
```

## 🔧 Step 5: Deploy and Test

1. **Deploy Backend**:
   - Click "Create Web Service"
   - Wait for build to complete (3-5 minutes)
   - Note your service URL

2. **Test Backend**:
   - Visit: `https://your-service-url.onrender.com/docs`
   - You should see FastAPI documentation
   - Visit: `https://your-service-url.onrender.com/health`
   - Should return: `{"status": "healthy", "environment": "production"}`

3. **Deploy Frontend** (if created):
   - Wait for build to complete
   - Test the frontend URL

## 🔗 Your URLs

After deployment, you'll have:

- **Backend API**: `https://your-backend-service.onrender.com`
- **API Documentation**: `https://your-backend-service.onrender.com/docs`
- **Health Check**: `https://your-backend-service.onrender.com/health`
- **Frontend** (if deployed): `https://your-frontend-service.onrender.com`

## 🧪 Test Your Deployment

1. **Test Backend API**:
   ```bash
   # Test health endpoint
   curl https://your-backend-service.onrender.com/health
   
   # Test API docs
   curl https://your-backend-service.onrender.com/docs
   ```

2. **Test Frontend** (if deployed):
   - Visit your frontend URL
   - Try to login
   - Create a test project

## 🔧 Troubleshooting

### Common Issues

1. **Build Fails**:
   - Check build logs in Render dashboard
   - Verify `requirements.txt` exists in backend folder
   - Check Python version compatibility

2. **Database Connection Error**:
   - Verify `DATABASE_URL` is correct
   - Check database is running
   - Ensure database URL includes credentials

3. **Service Not Starting**:
   - Check start command is correct
   - Verify `app.main:app` path
   - Check environment variables

4. **CORS Errors** (if testing frontend):
   - Update backend CORS settings
   - Add your frontend URL to allowed origins

### Debug Commands

```bash
# Check service logs
# Go to your service → "Logs" tab

# Test database connection
psql $DATABASE_URL -c "SELECT 1;"

# Check service status
curl https://your-service-url.onrender.com/health
```

## 📊 Monitor Your App

Render provides:
- **Real-time logs**
- **Performance metrics**
- **Deployment history**
- **Error tracking**

## 🔄 Updates

To update your app:
1. Push changes to GitHub
2. Render deploys automatically
3. Your app updates in minutes

## 🎉 You're Done!

Your Project Management Dashboard is now live on Render!

**Next Steps**:
1. Test all functionality
2. Set up monitoring
3. Configure custom domain (optional)
4. Share your app URL

## 🆘 Need Help?

- **Render Documentation**: https://render.com/docs
- **Render Support**: https://render.com/support
- **Community**: https://community.render.com

**Your app is now deployed and accessible worldwide!** 🌍 