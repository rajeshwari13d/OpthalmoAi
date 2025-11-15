# OpthalmoAI - Automated Setup and Deployment Guide

## 🚀 Quick Start (Automated)

### 1. Initial Setup
```bash
# Install root dependencies and setup workspaces
npm install

# Install all project dependencies (frontend + backend)
npm run install:all

# Build frontend for production
npm run build
```

### 2. Development Mode
```bash
# Start frontend only
npm start
# or
npm run start:frontend

# Start backend only (requires Python environment)
npm run start:backend

# Start both frontend and backend concurrently
npm run start:dev
```

### 3. Production Deployment
```bash
# Deploy frontend to Firebase
npm run deploy

# Deploy backend to Google Cloud Run (requires gcloud CLI)
npm run deploy:backend
```

## 🔧 Manual Setup Instructions

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Backend Setup
```bash
cd backend
# Create virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Available Scripts

| Command | Description |
|---------|-------------|
| `npm start` | Start frontend development server |
| `npm run start:backend` | Start backend API server |
| `npm run start:dev` | Start both frontend and backend |
| `npm run build` | Build frontend for production |
| `npm run deploy` | Deploy frontend to Firebase |
| `npm run deploy:backend` | Deploy backend to Cloud Run |
| `npm run test` | Run frontend tests |
| `npm run lint` | Check code style |
| `npm run clean` | Clean node_modules and build files |

## 🌐 URLs

- **Frontend (Development)**: http://localhost:3000
- **Backend API (Development)**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Production Frontend**: https://opthalmoai.web.app

## 🛠️ Environment Configuration

### Backend Environment (.env)
```bash
# Copy example environment file
cd backend
cp .env.example .env
# Edit .env with your configuration
```

### Frontend Environment
```bash
# Environment is configured in src/config/firebase.ts
# Update API endpoints for production deployment
```

## 📦 Dependencies

### Frontend
- React 18+ with TypeScript
- TailwindCSS for styling
- Firebase for authentication and hosting
- React Router for navigation

### Backend
- FastAPI for API framework
- PyTorch for AI model inference
- SQLAlchemy for database ORM
- Uvicorn as ASGI server

## 🔐 Security & Compliance

- HIPAA-style data handling
- No permanent image storage
- Secure authentication with Firebase
- Medical disclaimers and compliance messaging

## 📱 Mobile Support

- Fully responsive design
- Touch-friendly interface
- Mobile-first approach
- Progressive Web App capabilities

## 🏥 Medical Features

- Diabetic retinopathy screening
- 5-stage classification (0-4)
- Confidence scoring
- Professional medical disclaimers
- Report generation and download

---

**🚀 Ready to start? Run `npm install && npm run setup` to get everything configured automatically!**