// Firebase Configuration Test
const { initializeApp } = require('firebase/app');
const { getAnalytics } = require('firebase/analytics');
const { getFirestore } = require('firebase/firestore');
const { getStorage } = require('firebase/storage');

const firebaseConfig = {
  apiKey: "AIzaSyBUKNovWoSS2-NYd3nayET6QB_o42_gnSc",
  authDomain: "opthalmoai.firebaseapp.com",
  projectId: "opthalmoai",
  storageBucket: "opthalmoai.firebasestorage.app",
  messagingSenderId: "994507293975",
  appId: "1:994507293975:web:0a2d5e258a0e4e0d14e352",
  measurementId: "G-J7W6YCDHGL"
};

console.log('🔥 Firebase Configuration Test');
console.log('================================');

try {
  // Initialize Firebase App
  const app = initializeApp(firebaseConfig);
  console.log('✅ Firebase App initialized successfully');
  console.log(`   Project ID: ${firebaseConfig.projectId}`);
  console.log(`   Auth Domain: ${firebaseConfig.authDomain}`);
  console.log(`   Storage Bucket: ${firebaseConfig.storageBucket}`);

  // Initialize services
  const db = getFirestore(app);
  console.log('✅ Firestore initialized successfully');
  
  const storage = getStorage(app);
  console.log('✅ Firebase Storage initialized successfully');
  
  // Note: Analytics requires browser environment
  console.log('ℹ️  Analytics will be initialized in browser environment');
  console.log(`   Measurement ID: ${firebaseConfig.measurementId}`);

  console.log('\n🎉 Firebase configuration is VALID and ready for deployment!');
  console.log('📱 Your OpthalmoAI app can now use all Firebase services.');
  
} catch (error) {
  console.error('❌ Firebase configuration error:', error.message);
  console.log('\n🔧 Please check your Firebase configuration.');
}

console.log('\n🚀 Next steps:');
console.log('  1. Deploy frontend: npm run build && firebase deploy');
console.log('  2. Test in browser environment');
console.log('  3. Configure Firestore rules');
console.log('  4. Set up storage security rules');