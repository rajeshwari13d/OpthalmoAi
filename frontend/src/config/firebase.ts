// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getStorage } from "firebase/storage";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBUKNovWoSS2-NYd3nayET6QB_o42_gnSc",
  authDomain: "opthalmoai.firebaseapp.com",
  projectId: "opthalmoai",
  storageBucket: "opthalmoai.firebasestorage.app",
  messagingSenderId: "994507293975",
  appId: "1:994507293975:web:0a2d5e258a0e4e0d14e352",
  measurementId: "G-J7W6YCDHGL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const storage = getStorage(app);
const db = getFirestore(app);

export { app, analytics, storage, db };