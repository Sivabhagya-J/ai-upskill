# Deployment Guide

This guide will help you deploy the Project Management Dashboard to production.

## Prerequisites

- [Vercel Account](https://vercel.com) (for frontend)
- [Railway Account](https://railway.app) or [Render Account](https://render.com) (for backend)
- [PostgreSQL Database](https://supabase.com or [Railway](https://railway.app))

## Step 1: Deploy Backend

### Option A: Deploy to Railway (Recommended)

1. **Create Railway Account**
   - Go to [Railway](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Add PostgreSQL Database**
   - Click "New" → "Database" → "PostgreSQL"
   - Note down the database URL

4. **Configure Environment Variables**
   - Go to your backend service
   - Add the following environment variables:
   ```
   DATABASE_URL=your_postgresql_url_from_railway
   SECRET_KEY=your_super_secret_key_here
   ENVIRONMENT=production
   DEBUG=false
   ```

5. **Deploy**
   - Railway will automatically deploy when you push to your main branch
   - Your backend URL will be: `https://your-app-name.railway.app`

### Option B: Deploy to Render

1. **Create Render Account**
   - Go to [Render](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Add PostgreSQL Database**
   - Click "New" → "PostgreSQL"
   - Note down the database URL

4. **Configure Environment Variables**
   ```
   DATABASE_URL=your_postgresql_url_from_render
   SECRET_KEY=your_super_secret_key_here
   ENVIRONMENT=production
   DEBUG=false
   ```

## Step 2: Deploy Frontend to Vercel

1. **Create Vercel Account**
   - Go to [Vercel](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "New Project"
   - Import your GitHub repository
   - Set the root directory to `frontend`

3. **Configure Build Settings**
   - Framework Preset: `Vite`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Add Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add: `VITE_API_URL=https://your-backend-url.com/api/v1`
   - Replace `your-backend-url.com` with your actual backend URL

5. **Deploy**
   - Click "Deploy"
   - Your frontend will be available at: `https://your-app-name.vercel.app`

## Step 3: Update CORS Settings

After deploying both frontend and backend, update the CORS settings in your backend:

1. **Get your Vercel domain**
   - Your Vercel app URL will be something like: `https://your-app-name.vercel.app`

2. **Update backend CORS**
   - Go to your backend deployment (Railway/Render)
   - Add environment variable:
   ```
   BACKEND_CORS_ORIGINS=https://your-app-name.vercel.app
   ```

## Step 4: Test Deployment

1. **Test Backend**
   - Visit: `https://your-backend-url.com/docs`
   - You should see the FastAPI documentation

2. **Test Frontend**
   - Visit: `https://your-app-name.vercel.app`
   - Try to login and create a project

3. **Test API Connection**
   - Open browser dev tools
   - Check Network tab for API calls
   - Ensure no CORS errors

## Environment Variables Reference

### Backend Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
ENVIRONMENT=production
DEBUG=false
API_V1_STR=/api/v1

# CORS
BACKEND_CORS_ORIGINS=https://your-frontend-domain.com

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Frontend Environment Variables
```bash
# API Configuration
VITE_API_URL=https://your-backend-url.com/api/v1
```

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure your backend CORS settings include your frontend domain
   - Check that the protocol (http/https) matches

2. **Database Connection Issues**
   - Verify your DATABASE_URL is correct
   - Ensure your database is accessible from your backend deployment

3. **Build Failures**
   - Check that all dependencies are in requirements.txt
   - Verify Python version compatibility

4. **Environment Variables Not Working**
   - Restart your deployment after adding environment variables
   - Check variable names match exactly (case-sensitive)

### Debugging

1. **Backend Logs**
   - Railway: Go to your service → "Deployments" → "View Logs"
   - Render: Go to your service → "Logs"

2. **Frontend Logs**
   - Vercel: Go to your project → "Deployments" → "Functions" → "View Function Logs"

## Security Considerations

1. **Environment Variables**
   - Never commit secrets to your repository
   - Use strong, unique secret keys
   - Rotate keys regularly

2. **Database Security**
   - Use strong database passwords
   - Enable SSL connections
   - Restrict database access

3. **API Security**
   - Enable HTTPS only
   - Implement rate limiting
   - Validate all inputs

## Monitoring

1. **Set up monitoring**
   - Railway/Render provide basic monitoring
   - Consider adding external monitoring (Sentry, LogRocket)

2. **Health Checks**
   - Your backend has a `/health` endpoint
   - Monitor this endpoint for uptime

## Updates and Maintenance

1. **Deploying Updates**
   - Push to your main branch
   - Both Vercel and Railway/Render will auto-deploy

2. **Database Migrations**
   - For schema changes, you may need to run migrations manually
   - Consider using Alembic for database migrations

## Support

If you encounter issues:
1. Check the logs in your deployment platform
2. Verify all environment variables are set correctly
3. Test locally first to isolate issues
4. Check the troubleshooting section above 