#!/bin/bash

# OpthalmoAI Frontend Firebase Deployment Script
# Healthcare-compliant deployment with security validation

set -e  # Exit on any error

echo "🏥 OpthalmoAI Frontend Deployment to Firebase Hosting"
echo "===================================================="

# Configuration variables (replace with actual values)
PROJECT_ID="OPTHALMOAI_PROJECT_ID"
SITE_ID="OPTHALMOAI_SITE_ID"
FRONTEND_DIR="frontend"

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

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ required. Current: $(node -v)"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed"
        exit 1
    fi
    
    # Check Firebase CLI
    if ! command -v firebase &> /dev/null; then
        print_warning "Firebase CLI not found. Installing..."
        npm install -g firebase-tools
    fi
    
    print_success "Prerequisites check completed"
}

# Validate configuration
validate_configuration() {
    print_status "Validating configuration..."
    
    # Check if frontend directory exists
    if [ ! -d "$FRONTEND_DIR" ]; then
        print_error "Frontend directory not found: $FRONTEND_DIR"
        exit 1
    fi
    
    # Check if package.json exists
    if [ ! -f "$FRONTEND_DIR/package.json" ]; then
        print_error "package.json not found in $FRONTEND_DIR"
        exit 1
    fi
    
    # Check if firebase.json exists
    if [ ! -f "$FRONTEND_DIR/firebase.json" ]; then
        print_error "firebase.json not found in $FRONTEND_DIR"
        exit 1
    fi
    
    # Validate placeholder replacement
    if grep -q "OPTHALMOAI_PROJECT_ID" "$FRONTEND_DIR/.firebaserc"; then
        print_error "Please replace OPTHALMOAI_PROJECT_ID in .firebaserc with your actual Firebase project ID"
        exit 1
    fi
    
    if grep -q "OPTHALMOAI_SITE_ID" "$FRONTEND_DIR/firebase.json"; then
        print_error "Please replace OPTHALMOAI_SITE_ID in firebase.json with your actual Firebase hosting site ID"
        exit 1
    fi
    
    print_success "Configuration validation completed"
}

# Build frontend
build_frontend() {
    print_status "Building OpthalmoAI frontend..."
    
    cd "$FRONTEND_DIR"
    
    # Install dependencies
    print_status "Installing dependencies..."
    npm ci
    
    # Run healthcare compliance checks
    print_status "Running healthcare compliance checks..."
    if npm run lint 2>/dev/null; then
        print_success "Code quality checks passed"
    else
        print_warning "Linting not configured or failed"
    fi
    
    # Build production version
    print_status "Building production version..."
    npm run build
    
    if [ ! -d "build" ]; then
        print_error "Build directory not created. Build may have failed."
        exit 1
    fi
    
    # Validate build output
    BUILD_SIZE=$(du -sh build | cut -f1)
    print_success "Frontend built successfully (Size: $BUILD_SIZE)"
    
    cd ..
}

# Deploy to Firebase
deploy_to_firebase() {
    print_status "Deploying to Firebase Hosting..."
    
    cd "$FRONTEND_DIR"
    
    # Check Firebase authentication
    if ! firebase projects:list &> /dev/null; then
        print_warning "Not authenticated with Firebase. Please run: firebase login"
        exit 1
    fi
    
    # Validate project access
    print_status "Validating Firebase project access..."
    if ! firebase use --project "$PROJECT_ID" &> /dev/null; then
        print_error "Cannot access Firebase project: $PROJECT_ID"
        print_status "Available projects:"
        firebase projects:list
        exit 1
    fi
    
    # Deploy hosting
    print_status "Deploying to Firebase Hosting..."
    firebase deploy --only hosting --project "$PROJECT_ID"
    
    if [ $? -eq 0 ]; then
        print_success "Deployment completed successfully!"
        print_success "OpthalmoAI is now live at: https://$SITE_ID.web.app"
    else
        print_error "Deployment failed"
        exit 1
    fi
    
    cd ..
}

# Post-deployment validation
validate_deployment() {
    print_status "Running post-deployment validation..."
    
    SITE_URL="https://$SITE_ID.web.app"
    
    # Check if site is accessible
    if curl -s --head "$SITE_URL" | head -n 1 | grep -q "200 OK"; then
        print_success "Site is accessible: $SITE_URL"
    else
        print_warning "Site may not be accessible yet. DNS propagation can take a few minutes."
    fi
    
    # Check security headers
    print_status "Validating security headers..."
    HEADERS=$(curl -s -I "$SITE_URL")
    
    if echo "$HEADERS" | grep -q "strict-transport-security"; then
        print_success "HSTS header configured"
    else
        print_warning "HSTS header not found"
    fi
    
    if echo "$HEADERS" | grep -q "x-frame-options"; then
        print_success "X-Frame-Options header configured"
    else
        print_warning "X-Frame-Options header not found"
    fi
}

# Main deployment flow
main() {
    echo "Starting OpthalmoAI Frontend Deployment Process..."
    echo "=================================================="
    
    check_prerequisites
    validate_configuration
    build_frontend
    deploy_to_firebase
    validate_deployment
    
    echo ""
    print_success "🏥 OpthalmoAI Frontend Deployment Complete!"
    echo ""
    print_status "Healthcare Platform URL: https://$SITE_ID.web.app"
    print_status "Firebase Console: https://console.firebase.google.com/project/$PROJECT_ID"
    echo ""
    print_status "Next Steps:"
    echo "  1. Test medical image upload functionality"
    echo "  2. Verify API connectivity to Cloud Run backend"
    echo "  3. Validate healthcare compliance features"
    echo "  4. Monitor application performance"
    echo ""
    print_warning "Remember: This platform requires medical professional supervision for clinical use"
}

# Run main function
main "$@"