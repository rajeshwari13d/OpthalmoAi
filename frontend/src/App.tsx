// OpthalmoAI v2.0.1 - Cache Bust Build 20251116-2000 - PRODUCTION FIX
import React, { useState } from 'react';
import './App.css';
import './index.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import SplashScreen from './components/SplashScreen';
import GoogleSignIn from './components/GoogleSignIn';
import Dashboard from './components/Dashboard';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import RetinalUploadPage from './pages/RetinalUploadPage';
import CameraCapturePage from './pages/CameraCapturePage';
import ResultsPage from './pages/ResultsPage';
import ReportsPage from './pages/ReportsPage';

// Main App Content Component
const AppContent: React.FC = () => {
  const { user, loading } = useAuth();
  const [showSplash, setShowSplash] = useState(true);

  const handleSplashComplete = () => {
    setTimeout(() => {
      setShowSplash(false);
    }, 300); // Small delay for smooth transition
  };

  const handleSignInSuccess = (user: any) => {
    // User state will be automatically updated by AuthContext
    console.log('User signed in:', user.displayName);
  };

  // Show splash screen first
  if (showSplash) {
    return <SplashScreen onComplete={handleSplashComplete} />;
  }

  // Show loading state while checking auth
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-medical-600 via-clinical-600 to-health-600 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Checking authentication...</p>
        </div>
      </div>
    );
  }

  // If user is not authenticated, show sign-in
  if (!user) {
    return <GoogleSignIn onSignInSuccess={handleSignInSuccess} />;
  }

  // If user is authenticated, show dashboard or app content
  return (
    <Router>
      <div className="App min-h-screen bg-clinical-50 retinal-pattern">
        <Routes>
          {/* Dashboard Route */}
          <Route 
            path="/" 
            element={<Dashboard user={user} />} 
          />
          
          {/* Protected App Routes with Layout */}
          <Route 
            path="/home" 
            element={
              <Layout>
                <HomePage />
              </Layout>
            } 
          />
          <Route 
            path="/upload" 
            element={
              <Layout>
                <RetinalUploadPage />
              </Layout>
            } 
          />
          <Route 
            path="/capture" 
            element={
              <Layout>
                <CameraCapturePage />
              </Layout>
            } 
          />
          <Route 
            path="/results/:id" 
            element={
              <Layout>
                <ResultsPage />
              </Layout>
            } 
          />
          <Route 
            path="/reports" 
            element={
              <Layout>
                <ReportsPage />
              </Layout>
            } 
          />
          
          {/* Analytics route (placeholder) */}
          <Route 
            path="/analytics" 
            element={
              <Layout>
                <div className="container mx-auto px-4 py-8">
                  <h1 className="text-3xl font-bold text-gray-800 mb-6">Analytics Dashboard</h1>
                  <div className="bg-white rounded-lg shadow-md p-6">
                    <p className="text-gray-600">Analytics features coming soon...</p>
                  </div>
                </div>
              </Layout>
            } 
          />
        </Routes>
      </div>
    </Router>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;