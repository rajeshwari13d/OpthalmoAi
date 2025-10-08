# OpthalmoAI - AI-Driven Predictive Ophthalmology Platform

## Project Overview
OpthalmoAI is a React-based web application focused on diabetic retinopathy screening. It's an AI-driven platform that allows users to upload or capture retinal fundus images for automated analysis and risk assessment.

## Architecture
- **Frontend**: React with TailwindCSS and shadcn/ui components
- **Backend**: Python FastAPI with PyTorch/TensorFlow model inference
- **Database**: Secure image storage with anonymization
- **Deployment**: Docker containerized, cloud-ready

## Key Features
- Image upload and camera capture functionality
- AI-powered diabetic retinopathy detection (stages 0-4)
- Risk assessment with confidence scoring
- Printable/downloadable patient reports
- Healthcare compliance (HIPAA-style privacy)
- Medical disclaimers and professional guidance

## Development Stack
- React, TailwindCSS, shadcn/ui
- Python, FastAPI, OpenCV, Pillow
- PyTorch/TensorFlow for model inference
- Docker for containerization
- Healthcare-friendly design with white/blue/green theme

## Medical Compliance Requirements
- Clear disclaimers: assistive screening tool, not diagnostic substitute
- Secure image handling and anonymization
- HIPAA-style privacy standards
- Ethical AI standards in healthcare

## MVP Development Roadmap
1. Frontend interface with upload/camera capture (Week 1-2)
2. Backend inference API and model integration (Week 3-4)
3. Results display and report generation (Week 5)
4. Testing and deployment (Week 6)

## Code Guidelines
- Use healthcare-friendly design patterns
- Implement proper error handling and validation
- Follow security best practices for medical data
- Include comprehensive medical disclaimers
- Ensure accessibility compliance