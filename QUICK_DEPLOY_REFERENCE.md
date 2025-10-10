# 🚀 OpthalmoAI Quick Deployment Reference

## ⚡ **One-Command Deployment**

### Windows
```cmd
scripts\deploy-frontend.bat
```

### Linux/Mac  
```bash
./scripts/deploy-frontend.sh
```

---

## 📝 **Configuration Checklist**

### Before First Deployment
- [ ] Replace `OPTHALMOAI_PROJECT_ID` in `.firebaserc`
- [ ] Replace `OPTHALMOAI_SITE_ID` in `firebase.json` 
- [ ] Run `firebase login` to authenticate
- [ ] Verify `firebase projects:list` shows your project

### Manual Deployment
```bash
cd frontend
npm run build
firebase deploy --only hosting --project YOUR_PROJECT_ID
```

---

## 🏥 **Healthcare Features**

✅ **Medical Disclaimers** - Professional guidance throughout
✅ **Security Headers** - HIPAA-style protection  
✅ **AI Analysis** - 5-stage diabetic retinopathy detection
✅ **Emergency Detection** - Critical case flagging
✅ **Clinical Reports** - Professional medical documentation

---

## 🔗 **Key URLs**

- **Live Site**: `https://YOUR_SITE_ID.web.app`
- **Firebase Console**: `https://console.firebase.google.com/project/YOUR_PROJECT_ID`
- **API Backend**: `https://us-central1-opthalmoai-api-a.run.app`

---

## 🆘 **Quick Troubleshooting**

### Site Not Loading
```bash
firebase hosting:sites:list  # Verify site ID
firebase deploy --debug     # Detailed deployment logs
```

### API Not Working
- Check Cloud Run service is deployed
- Verify CORS settings in backend
- Check browser network tab for errors

### Build Errors
```bash
cd frontend
npm ci                # Clean install
rm -rf node_modules   # Reset if needed
npm run build         # Test build
```

---

**🏥 OpthalmoAI: Ready for Healthcare Deployment!** ✨