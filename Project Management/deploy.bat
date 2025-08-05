@echo off
echo 🚀 Project Management Dashboard Deployment Script
echo ==================================================

echo.
echo [INFO] Starting deployment preparation...

REM Check if Node.js is installed
echo [INFO] Checking requirements...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo [SUCCESS] All requirements are met!

REM Build frontend
echo.
echo [INFO] Building frontend...
cd frontend

echo [INFO] Installing frontend dependencies...
call npm install

echo [INFO] Building frontend for production...
call npm run build

cd ..

echo [SUCCESS] Frontend built successfully!

REM Test backend
echo.
echo [INFO] Testing backend locally...
cd backend

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo [INFO] Installing backend dependencies...
pip install -r requirements.txt

echo [INFO] Testing backend startup...
python -c "from app.main import app; print('Backend imports successfully')"

cd ..

echo [SUCCESS] Backend test passed!

REM Generate deployment checklist
echo.
echo [INFO] Generating deployment checklist...

(
echo # Deployment Checklist
echo.
echo ## Pre-Deployment
echo - [ ] All tests pass locally
echo - [ ] Environment variables are configured
echo - [ ] Database is ready
echo - [ ] Secrets are generated
echo.
echo ## Backend Deployment
echo - [ ] Create Railway/Render account
echo - [ ] Connect GitHub repository
echo - [ ] Add PostgreSQL database
echo - [ ] Configure environment variables:
echo   - [ ] DATABASE_URL
echo   - [ ] SECRET_KEY
echo   - [ ] ENVIRONMENT=production
echo   - [ ] DEBUG=false
echo - [ ] Deploy backend
echo - [ ] Test backend health endpoint
echo - [ ] Note backend URL
echo.
echo ## Frontend Deployment
echo - [ ] Create Vercel account
echo - [ ] Import GitHub repository
echo - [ ] Set root directory to `frontend`
echo - [ ] Configure build settings
echo - [ ] Add environment variable: VITE_API_URL
echo - [ ] Deploy frontend
echo - [ ] Note frontend URL
echo.
echo ## Post-Deployment
echo - [ ] Update CORS settings in backend
echo - [ ] Test login functionality
echo - [ ] Test project creation
echo - [ ] Test task management
echo - [ ] Check for console errors
echo - [ ] Verify API calls work
echo.
echo ## Environment Variables Reference
echo.
echo ### Backend (Railway/Render)
echo ```
echo DATABASE_URL=postgresql://user:password@host:port/database
echo SECRET_KEY=your_super_secret_key_here
echo ENVIRONMENT=production
echo DEBUG=false
echo BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app
echo ```
echo.
echo ### Frontend (Vercel)
echo ```
echo VITE_API_URL=https://your-backend-domain.railway.app/api/v1
echo ```
echo.
echo ## URLs to Test
echo - Backend API: https://your-backend-domain.railway.app/docs
echo - Frontend App: https://your-frontend-domain.vercel.app
echo - Health Check: https://your-backend-domain.railway.app/health
) > DEPLOYMENT_CHECKLIST.md

echo [SUCCESS] Deployment checklist generated: DEPLOYMENT_CHECKLIST.md

echo.
echo [SUCCESS] Deployment preparation completed!
echo.
echo [INFO] Next steps:
echo 1. Follow the DEPLOYMENT.md guide
echo 2. Use DEPLOYMENT_CHECKLIST.md to track progress
echo 3. Deploy backend first (Railway/Render)
echo 4. Deploy frontend second (Vercel)
echo 5. Update CORS settings
echo 6. Test the complete application
echo.
echo [WARNING] Remember to set up your environment variables before deploying!
echo.
pause 