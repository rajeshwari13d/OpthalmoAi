# OpthalmoAI - AI-Driven Predictive Ophthalmology Platform

## Overview

OpthalmoAI is a comprehensive React-based web application focused on diabetic retinopathy screening. This AI-driven platform enables users to upload or capture retinal fundus images for automated analysis and risk assessment, providing healthcare professionals and patients with valuable insights into diabetic retinopathy progression.

## 🏥 Healthcare Compliance

**⚠️ IMPORTANT MEDICAL DISCLAIMER**
This application is designed as an **assistive screening tool** and is **NOT a substitute for professional medical diagnosis**. All results should be reviewed by qualified healthcare professionals.

- **HIPAA-style Privacy**: Secure image handling and data anonymization
- **Ethical AI Standards**: Responsible AI implementation in healthcare
- **Medical Disclaimers**: Clear communication about tool limitations
- **Professional Guidance**: Emphasis on healthcare professional consultation

## 🏗️ Architecture

### Frontend
- **React 18** with TypeScript
- **TailwindCSS** for styling
- **shadcn/ui** component library
- Healthcare-friendly design (white/blue/green theme)
- Responsive design for various devices

### Backend
- **FastAPI** with Python 3.13
- **PyTorch/TensorFlow** for model inference
- **OpenCV & Pillow** for image preprocessing
- **Uvicorn** ASGI server
- RESTful API design

### AI Model
- Pre-trained **ResNet50/VGG16** CNN
- Fine-tuned on Kaggle Diabetic Retinopathy Detection dataset
- Predicts stages 0-4 of diabetic retinopathy
- Confidence scoring and risk assessment

### Deployment
- **Docker** containerized application
- **Docker Compose** for multi-service orchestration
- Cloud-ready architecture
- Scalable infrastructure

## 📁 Project Structure

```
OpthalmoAI/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ui/          # shadcn/ui components
│   │   │   ├── ImageUpload.tsx
│   │   │   ├── CameraCapture.tsx
│   │   │   ├── ResultsCard.tsx
│   │   │   └── ReportGenerator.tsx
│   │   ├── pages/           # Application pages
│   │   │   ├── HomePage.tsx
│   │   │   ├── ResultsPage.tsx
│   │   │   └── ReportsPage.tsx
│   │   └── services/        # API service layer
│   ├── public/
│   └── package.json
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/             # API endpoints
│   │   │   └── endpoints/
│   │   │       ├── health.py
│   │   │       └── prediction.py
│   │   ├── core/            # Core configuration
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── models/          # AI models and data models
│   │   │   ├── dr_model.py
│   │   │   └── schemas.py
│   │   └── main.py          # FastAPI app entry point
│   └── requirements.txt
├── docker-compose.yml        # Multi-service orchestration
├── Dockerfile.frontend       # Frontend container
├── Dockerfile.backend        # Backend container
└── README.md
```

## 🚀 Getting Started

### Prerequisites

1. **Node.js** (v18 or higher) - for frontend development
2. **Python** (3.11 or higher) - for backend development
3. **Docker & Docker Compose** - for containerized deployment

### Development Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd OpthalmoAI
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```
The frontend will be available at `http://localhost:3000`

#### 3. Backend Setup
```bash
cd backend
# Create virtual environment (automatically configured in this project)
# Install dependencies (automatically installed: fastapi, uvicorn, torch, opencv-python, pillow, etc.)
```

#### 4. Start Backend Server
Use VS Code tasks or run manually:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
The backend API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### 🐳 Docker Deployment

#### Build and Start Services
```bash
docker-compose up -d --build
```

#### Stop Services
```bash
docker-compose down
```

## 🛠️ VS Code Development

This project includes pre-configured VS Code tasks:

1. **Start Frontend Development Server** - Launches React dev server
2. **Start Backend FastAPI Server** - Launches FastAPI with hot reload
3. **Install Frontend Dependencies** - Runs npm install
4. **Build Docker Images** - Builds all Docker containers
5. **Start Docker Services** - Launches full stack with Docker
6. **Stop Docker Services** - Stops Docker containers

Access tasks via: `Ctrl+Shift+P` → "Tasks: Run Task"

## 🧪 Key Features

### Image Processing
- **Upload Support**: Various image formats (JPEG, PNG, TIFF)
- **Camera Capture**: Live retinal scan capture
- **Image Validation**: Format, size, and quality checks
- **Preprocessing**: Automated image enhancement for analysis

### AI Analysis
- **Diabetic Retinopathy Detection**: Stages 0-4 classification
- **Confidence Scoring**: Model certainty assessment
- **Risk Stratification**: Low, moderate, high risk levels
- **Quality Assurance**: Image quality scoring

### Results & Reporting
- **Intuitive Results Display**: Easy-to-read analysis cards
- **Detailed Reporting**: Comprehensive patient reports
- **Print/Download**: PDF generation for medical records
- **Medical Disclaimers**: Integrated compliance messaging

### Security & Compliance
- **Image Anonymization**: Automatic PII removal
- **Secure Storage**: Encrypted image handling
- **CORS Configuration**: Secure cross-origin requests
- **Input Validation**: Comprehensive request validation

## 📊 MVP Development Roadmap

- **Week 1-2**: ✅ Frontend interface with upload/camera capture
- **Week 3-4**: 🔄 Backend inference API and model integration
- **Week 5**: 📋 Results display and report generation
- **Week 6**: 🧪 Testing and deployment

## 🤝 Healthcare Provider Dashboard (Future)
- Patient history tracking
- Clinical recommendation system
- Batch analysis capabilities
- Integration with EHR systems

## 🔧 Environment Variables

Create `.env` files for configuration:

### Backend (.env)
```
SECRET_KEY=your-secret-key-here
API_V1_STR=/api/v1
PROJECT_NAME=OpthalmoAI
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
```

## 🧑‍💻 Development Guidelines

1. **Medical Compliance**: Always include medical disclaimers
2. **Security First**: Implement proper data handling
3. **Accessibility**: Ensure WCAG compliance
4. **Error Handling**: Comprehensive validation and error management
5. **Testing**: Unit tests for critical components
6. **Documentation**: Clear code documentation and API specs

## 📄 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints
- `GET /api/v1/health` - Health check
- `POST /api/v1/predict` - Image analysis
- `GET /api/v1/report/{id}` - Generate reports

## 🤖 Model Information

The AI model is designed to:
- Analyze retinal fundus images
- Detect diabetic retinopathy severity (0-4 scale)
- Provide confidence scores
- Suggest follow-up recommendations

**Model Disclaimer**: This model is trained for screening purposes and requires validation by healthcare professionals.

## 🆘 Troubleshooting

### Common Issues

1. **Backend Import Errors**: Ensure all Python packages are installed
2. **CORS Issues**: Check frontend/backend URL configuration
3. **Docker Build Failures**: Verify Dockerfile syntax and dependencies
4. **Node.js Missing**: Install Node.js for frontend development

### Support
For development support, refer to the project documentation or contact the development team.

---

**Remember**: This is a healthcare application. Always prioritize patient safety, data privacy, and regulatory compliance in all development activities.