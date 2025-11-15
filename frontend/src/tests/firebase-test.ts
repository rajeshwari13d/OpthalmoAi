// Firebase Configuration Test
// This file tests the Firebase setup and connection

import { app, analytics, storage, db } from '../config/firebase';
import { getAuth } from 'firebase/auth';

// Test Firebase App Initialization
console.log('Testing Firebase Configuration...');

try {
  // Test App
  if (app) {
    console.log('✅ Firebase App initialized successfully');
    console.log('📋 App Name:', app.name);
    console.log('🔧 App Options:', app.options);
  } else {
    console.error('❌ Firebase App failed to initialize');
  }

  // Test Analytics
  if (analytics) {
    console.log('✅ Firebase Analytics initialized successfully');
  } else {
    console.log('⚠️ Firebase Analytics not available (normal in development)');
  }

  // Test Storage
  if (storage) {
    console.log('✅ Firebase Storage initialized successfully');
    console.log('📁 Storage Bucket:', storage.app.options.storageBucket);
  } else {
    console.error('❌ Firebase Storage failed to initialize');
  }

  // Test Firestore
  if (db) {
    console.log('✅ Firebase Firestore initialized successfully');
    console.log('🗄️ Firestore App:', db.app.name);
  } else {
    console.error('❌ Firebase Firestore failed to initialize');
  }

  // Test Auth (optional)
  try {
    const auth = getAuth(app);
    if (auth) {
      console.log('✅ Firebase Auth initialized successfully');
    }
  } catch (error) {
    console.log('⚠️ Firebase Auth not configured (optional)');
  }

  console.log('\n🎉 Firebase Configuration Test Complete!');
  console.log('📊 Project ID:', app.options.projectId);
  console.log('🔑 API Key:', app.options.apiKey ? 'Configured' : 'Missing');
  console.log('🌐 Auth Domain:', app.options.authDomain);
  console.log('📁 Storage Bucket:', app.options.storageBucket);

} catch (error) {
  console.error('❌ Firebase Configuration Error:', error);
}

export {};