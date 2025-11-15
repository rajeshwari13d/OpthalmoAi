# GitHub Repository Secrets Setup

## Required Secrets for CI/CD Pipeline

To enable automated deployment through GitHub Actions, you need to set up the following secrets in your GitHub repository:

### 🔐 Setting Up GitHub Secrets

1. **Go to your GitHub repository**
2. **Navigate to**: Settings → Secrets and variables → Actions
3. **Click**: "New repository secret"
4. **Add the following secrets**:

### 📋 Required Secrets

#### `FIREBASE_SERVICE_ACCOUNT`
```json
{
  "type": "service_account",
  "project_id": "opthalmoai",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxxx@opthalmoai.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40opthalmoai.iam.gserviceaccount.com"
}
```

**How to get this:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your OpthalmoAI project
3. Go to Project Settings → Service Accounts
4. Click "Generate new private key"
5. Copy the entire JSON content
6. Paste as the secret value

---

## 🚀 Automated Deployment Workflow

Once secrets are configured, the deployment workflow will:

### ✅ **Trigger Conditions:**
- Push to `main` branch
- Pull request merge to `main`

### 🔄 **Deployment Steps:**
1. **Checkout code** from repository
2. **Setup Node.js** environment (v20)
3. **Cache dependencies** for faster builds
4. **Install dependencies** (`npm ci`)
5. **Build production** optimized bundle
6. **Deploy to Firebase Hosting** automatically

### 📊 **Build Results:**
- **Live URL**: https://opthalmoai.web.app
- **Build artifacts**: Stored in GitHub Actions
- **Deploy status**: Visible in GitHub Actions tab

---

## 🛠️ Manual Deployment (Alternative)

If you prefer manual deployment or need to troubleshoot:

### Frontend Deployment:
```bash
cd frontend
npm run build
firebase deploy --only hosting
```

### Backend Deployment:
```bash
# Use the automated script
scripts\deploy-backend.bat

# Or manual steps:
cd backend
docker build -t opthalmoai-backend .
# ... follow Cloud Run deployment steps
```

---

## 🔍 Troubleshooting

### Common Issues:

#### ❌ **"Invalid service account" error**
- **Solution**: Verify the Firebase service account JSON is valid
- **Check**: Project ID matches your Firebase project
- **Ensure**: Service account has Firebase Admin permissions

#### ❌ **"Permission denied" error**
- **Solution**: Service account needs "Firebase Admin" and "Editor" roles
- **Fix**: Add roles in Google Cloud Console IAM & Admin

#### ❌ **Build fails with dependency errors**
- **Solution**: Clear cache and reinstall dependencies
- **Commands**: 
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

#### ❌ **Deployment succeeds but app doesn't work**
- **Check**: API URLs in production environment variables
- **Verify**: CORS settings include production domain
- **Ensure**: All environment variables are properly set

---

## 🎯 Deployment Checklist

### Before First Deployment:
- [ ] Firebase project created and configured
- [ ] GitHub repository secrets added
- [ ] Service account has proper permissions
- [ ] Production environment variables configured
- [ ] Frontend built successfully locally
- [ ] Backend tested locally

### For Each Deployment:
- [ ] Code changes tested locally
- [ ] No build errors or warnings
- [ ] Environment variables updated if needed
- [ ] API endpoints accessible
- [ ] Medical disclaimers and compliance messages current

### After Deployment:
- [ ] Live site accessible at https://opthalmoai.web.app
- [ ] All pages load correctly
- [ ] Image upload functionality works
- [ ] API calls successful (or demo mode working)
- [ ] Mobile responsiveness verified
- [ ] Medical disclaimers visible

---

## 📞 Support

If you encounter issues:

1. **Check GitHub Actions logs** for detailed error messages
2. **Verify Firebase Console** for deployment status
3. **Test locally** to isolate environment-specific issues
4. **Review secrets configuration** for typos or missing data

---

## 🎉 Success Indicators

**✅ Deployment is successful when:**
- GitHub Actions workflow shows green checkmark
- Live site loads at https://opthalmoai.web.app
- All components render correctly
- Navigation works across all pages
- Upload interface is functional
- Medical disclaimers are displayed
- Mobile responsive design works properly

**🎯 Ready for healthcare professional demonstrations!**