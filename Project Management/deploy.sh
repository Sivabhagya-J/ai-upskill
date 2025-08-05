#!/bin/bash

# Project Management Dashboard Deployment Script
# This script helps prepare and deploy the application

set -e

echo "🚀 Project Management Dashboard Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install git first."
        exit 1
    fi
    
    # Check if node is installed
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Check if npm is installed
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    print_success "All requirements are met!"
}

# Build frontend
build_frontend() {
    print_status "Building frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing frontend dependencies..."
    npm install
    
    # Build the project
    print_status "Building frontend for production..."
    npm run build
    
    cd ..
    
    print_success "Frontend built successfully!"
}

# Test backend locally
test_backend() {
    print_status "Testing backend locally..."
    
    cd backend
    
    # Check if Python is installed
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed. Please install Python first."
        exit 1
    fi
    
    # Install dependencies
    print_status "Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Test if the app can start
    print_status "Testing backend startup..."
    python -c "from app.main import app; print('Backend imports successfully')"
    
    cd ..
    
    print_success "Backend test passed!"
}

# Generate deployment checklist
generate_checklist() {
    print_status "Generating deployment checklist..."
    
    cat > DEPLOYMENT_CHECKLIST.md << 'EOF'
# Deployment Checklist

## Pre-Deployment
- [ ] All tests pass locally
- [ ] Environment variables are configured
- [ ] Database is ready
- [ ] Secrets are generated

## Backend Deployment
- [ ] Create Railway/Render account
- [ ] Connect GitHub repository
- [ ] Add PostgreSQL database
- [ ] Configure environment variables:
  - [ ] DATABASE_URL
  - [ ] SECRET_KEY
  - [ ] ENVIRONMENT=production
  - [ ] DEBUG=false
- [ ] Deploy backend
- [ ] Test backend health endpoint
- [ ] Note backend URL

## Frontend Deployment
- [ ] Create Vercel account
- [ ] Import GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Configure build settings
- [ ] Add environment variable: VITE_API_URL
- [ ] Deploy frontend
- [ ] Note frontend URL

## Post-Deployment
- [ ] Update CORS settings in backend
- [ ] Test login functionality
- [ ] Test project creation
- [ ] Test task management
- [ ] Check for console errors
- [ ] Verify API calls work

## Environment Variables Reference

### Backend (Railway/Render)
```
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your_super_secret_key_here
ENVIRONMENT=production
DEBUG=false
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

### Frontend (Vercel)
```
VITE_API_URL=https://your-backend-domain.railway.app/api/v1
```

## URLs to Test
- Backend API: https://your-backend-domain.railway.app/docs
- Frontend App: https://your-frontend-domain.vercel.app
- Health Check: https://your-backend-domain.railway.app/health
EOF

    print_success "Deployment checklist generated: DEPLOYMENT_CHECKLIST.md"
}

# Main deployment function
main() {
    echo ""
    print_status "Starting deployment preparation..."
    
    # Check requirements
    check_requirements
    
    # Build frontend
    build_frontend
    
    # Test backend
    test_backend
    
    # Generate checklist
    generate_checklist
    
    echo ""
    print_success "Deployment preparation completed!"
    echo ""
    print_status "Next steps:"
    echo "1. Follow the DEPLOYMENT.md guide"
    echo "2. Use DEPLOYMENT_CHECKLIST.md to track progress"
    echo "3. Deploy backend first (Railway/Render)"
    echo "4. Deploy frontend second (Vercel)"
    echo "5. Update CORS settings"
    echo "6. Test the complete application"
    echo ""
    print_warning "Remember to set up your environment variables before deploying!"
}

# Run main function
main "$@" 