# Production Configuration Guide

## Environment Setup

### Backend Configuration

1. **Copy the environment template:**
   ```bash
   cp backend/.env.example backend/.env
   ```

2. **Update the following critical settings in `backend/.env`:**
   - `SECRET_KEY`: Generate a strong, unique secret key
   - `BACKEND_CORS_ORIGINS`: Add your production frontend domain
   - `MODEL_PATH`: Ensure the trained model file exists
   - `DATABASE_URL`: Configure if using database storage

3. **Required environment variables for production:**
   ```bash
   # Security - CRITICAL TO CHANGE
   SECRET_KEY=your-super-secure-random-key-here
   
   # API Settings
   PROJECT_NAME=OpthalmoAI
   DEBUG=false
   ENVIRONMENT=production
   
   # CORS - Add your domains
   BACKEND_CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
   
   # Model Configuration
   MODEL_PATH=app/models/diabetic_retinopathy_model.pth
   MODEL_TYPE=resnet50
   
   # File Upload
   MAX_FILE_SIZE=10485760
   UPLOAD_DIRECTORY=/app/uploads
   ```

### Frontend Configuration

1. **Copy the environment template:**
   ```bash
   cp frontend/.env.example frontend/.env.production
   ```

2. **Update the following settings in `frontend/.env.production`:**
   - `REACT_APP_API_BASE_URL`: Your production API domain
   - Analytics tracking IDs
   - Privacy and terms URLs

3. **Required environment variables for production:**
   ```bash
   # API Configuration
   REACT_APP_API_BASE_URL=https://api.yourdomain.com
   REACT_APP_API_VERSION=v1
   
   # App Settings
   REACT_APP_DEBUG_MODE=false
   REACT_APP_MOCK_API=false
   
   # Legal Compliance
   REACT_APP_PRIVACY_POLICY_URL=https://yourdomain.com/privacy
   REACT_APP_TERMS_OF_SERVICE_URL=https://yourdomain.com/terms
   ```

## Deployment Options

### Option 1: Docker Compose (Recommended)

1. **Update docker-compose.yml:**
   - Ensure environment files are correctly referenced
   - Update port mappings as needed
   - Configure volumes for persistent data

2. **Deploy:**
   ```bash
   docker-compose up -d --build
   ```

### Option 2: Manual Deployment

#### Backend Deployment:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend Deployment:
```bash
cd frontend
npm install
npm run build
# Serve the build folder with nginx or your preferred server
```

### Option 3: Cloud Deployment

#### AWS/GCP/Azure:
- Use container services (ECS, Cloud Run, Container Apps)
- Configure load balancers and SSL certificates
- Set up monitoring and logging

#### Firebase/Vercel (Frontend only):
```bash
cd frontend
npm run build
# Deploy using platform-specific CLI tools
```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Configure proper CORS origins
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up rate limiting
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Set up monitoring and alerts
- [ ] Implement backup strategy

## Monitoring and Health Checks

### Health Endpoints:
- Backend: `GET /api/v1/health`
- Model Status: `GET /api/v1/model-info`

### Recommended Monitoring:
- Application performance monitoring (APM)
- Error tracking (Sentry)
- Infrastructure monitoring
- Medical compliance audit logs

## Model Deployment

1. **Train your diabetic retinopathy model**
2. **Save the model file:**
   ```python
   torch.save(model.state_dict(), 'diabetic_retinopathy_model.pth')
   ```
3. **Place the model file in the configured MODEL_PATH**
4. **Update MODEL_TYPE in environment variables**

## Database Setup (Optional)

For persistent storage of analysis results:

```sql
-- PostgreSQL setup example
CREATE DATABASE opthalmoai;
CREATE USER opthalmo_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE opthalmoai TO opthalmo_user;
```

Update `DATABASE_URL` in backend/.env accordingly.

## Compliance Considerations

- Ensure HIPAA compliance for healthcare data
- Implement proper data anonymization
- Set up audit logging for all analysis requests
- Configure data retention policies
- Regular security assessments

## Troubleshooting

### Common Issues:
1. **Model not loading**: Check MODEL_PATH and file permissions
2. **CORS errors**: Verify BACKEND_CORS_ORIGINS configuration
3. **File upload failures**: Check MAX_FILE_SIZE and upload directory permissions
4. **API connection issues**: Verify REACT_APP_API_BASE_URL setting

### Logs:
- Backend logs: Check uvicorn/gunicorn logs
- Frontend logs: Browser console and build logs
- System logs: Docker/container platform logs