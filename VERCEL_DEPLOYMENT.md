# Quick Vercel Deployment Guide

This guide will help you deploy your Project Management Dashboard frontend to Vercel quickly.

## Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **Backend Deployed**: Your backend should be deployed first (Railway/Render)

## Important URLs

### Vercel Platform URLs
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Vercel Documentation**: https://vercel.com/docs
- **Vercel Support**: https://vercel.com/support
- **Vercel Community**: https://github.com/vercel/vercel/discussions
- **Vercel CLI**: https://vercel.com/docs/cli

### Backend Deployment URLs
- **Railway**: https://railway.app
- **Render**: https://render.com
- **Supabase (Database)**: https://supabase.com
- **Heroku**: https://heroku.com

### Database URLs
- **Railway PostgreSQL**: https://railway.app/database/postgresql
- **Render PostgreSQL**: https://render.com/docs/databases
- **Supabase**: https://supabase.com/database

## Step 1: Prepare Your Repository

1. **Run the deployment preparation script**:
   ```bash
   # On Windows
   deploy.bat
   
   # On Mac/Linux
   ./deploy.sh
   ```

2. **Commit and push your changes**:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

## Step 2: Deploy to Vercel

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Sign in with your GitHub account

2. **Import Your Project**
   - Click "New Project"
   - Select "Import Git Repository"
   - Choose your project repository

3. **Configure Project Settings**
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Add Environment Variables**
   - Click "Environment Variables"
   - Add: `VITE_API_URL` = `https://your-backend-url.com/api/v1`
   - Replace `your-backend-url.com` with your actual backend URL

5. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete

## Step 3: Configure Custom Domain (Optional)

1. **Go to Project Settings**
   - Click on your project
   - Go to "Settings" → "Domains"

2. **Add Custom Domain**
   - Enter your domain name
   - Follow Vercel's DNS configuration instructions

## Step 4: Update Backend CORS

After your frontend is deployed, update your backend CORS settings:

1. **Get your Vercel domain**
   - Your app will be at: `https://your-app-name.vercel.app`

2. **Update backend environment variables**
   - Go to your backend deployment (Railway/Render)
   - Add: `BACKEND_CORS_ORIGINS` = `https://your-app-name.vercel.app`

## Step 5: Test Your Deployment

1. **Visit your app**: `https://your-app-name.vercel.app`
2. **Test login functionality**
3. **Create a test project**
4. **Check browser console for errors**

## Troubleshooting

### Build Failures
- Check that all dependencies are in `package.json`
- Verify Node.js version compatibility
- Check build logs in Vercel dashboard

### API Connection Issues
- Verify `VITE_API_URL` is correct
- Check CORS settings in backend
- Ensure backend is running and accessible

### Environment Variables Not Working
- Restart deployment after adding variables
- Check variable names (case-sensitive)
- Verify variable values are correct

## Environment Variables Reference

### Required
```
VITE_API_URL=https://your-backend-url.com/api/v1
```

### Optional
```
VITE_APP_NAME=Project Management Dashboard
VITE_APP_VERSION=1.0.0
```

## Vercel Features

### Automatic Deployments
- Every push to main branch triggers a new deployment
- Preview deployments for pull requests

### Performance
- Global CDN
- Automatic HTTPS
- Edge functions support

### Analytics
- View deployment analytics
- Monitor performance
- Track usage

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)

## Next Steps

After successful deployment:
1. Set up monitoring and analytics
2. Configure custom domain
3. Set up CI/CD pipelines
4. Implement performance monitoring
5. Add error tracking (Sentry, LogRocket) 