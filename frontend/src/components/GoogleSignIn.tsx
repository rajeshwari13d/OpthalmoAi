import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth } from '../config/firebase';
import { Eye, Shield, Heart, AlertCircle, Loader2 } from 'lucide-react';

interface GoogleSignInProps {
  onSignInSuccess: (user: any) => void;
}

const GoogleSignIn: React.FC<GoogleSignInProps> = ({ onSignInSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGoogleSignIn = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const provider = new GoogleAuthProvider();
      provider.addScope('email');
      provider.addScope('profile');
      
      const result = await signInWithPopup(auth, provider);
      onSignInSuccess(result.user);
    } catch (error: any) {
      console.error('Google Sign-In Error:', error);
      
      // Handle specific error cases
      switch (error.code) {
        case 'auth/popup-closed-by-user':
          setError('Sign-in was cancelled. Please try again.');
          break;
        case 'auth/popup-blocked':
          setError('Pop-up blocked. Please allow pop-ups and try again.');
          break;
        case 'auth/network-request-failed':
          setError('Network error. Please check your connection.');
          break;
        default:
          setError('Sign-in failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-medical-600 via-clinical-600 to-health-600 flex items-center justify-center p-4">
      {/* Background Animation */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute top-20 left-20 w-40 h-40 bg-white/5 rounded-full"
          animate={{
            scale: [1, 1.3, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-20 right-20 w-32 h-32 bg-white/5 rounded-full"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.2, 0.4, 0.2],
          }}
          transition={{
            duration: 3.5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1,
          }}
        />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="w-full max-w-md mx-auto bg-white rounded-2xl shadow-2xl p-8 relative z-10"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mx-auto w-16 h-16 bg-gradient-to-br from-teal-50 to-blue-50 rounded-full shadow-lg border-2 border-teal-100 flex items-center justify-center mb-4"
          >
            <img 
              src="/opthalmo-icon.svg" 
              alt="OpthalmoAI" 
              className="w-12 h-12"
            />
          </motion.div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">
            Welcome to OpthalmoAI
          </h1>
          <p className="text-gray-600 text-sm">
            AI-Powered Diabetic Retinopathy Screening Platform
          </p>
        </div>

        {/* Healthcare Features */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="grid grid-cols-3 gap-4 mb-8"
        >
          <div className="text-center">
            <div className="w-12 h-12 bg-medical-100 rounded-full flex items-center justify-center mx-auto mb-2">
              <Eye className="w-6 h-6 text-medical-600" />
            </div>
            <p className="text-xs text-gray-600">AI Analysis</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-clinical-100 rounded-full flex items-center justify-center mx-auto mb-2">
              <Shield className="w-6 h-6 text-clinical-600" />
            </div>
            <p className="text-xs text-gray-600">HIPAA Secure</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-health-100 rounded-full flex items-center justify-center mx-auto mb-2">
              <Heart className="w-6 h-6 text-health-600" />
            </div>
            <p className="text-xs text-gray-600">Healthcare</p>
          </div>
        </motion.div>

        {/* Sign-In Section */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <h2 className="text-lg font-semibold text-gray-800 mb-4 text-center">
            Sign in to continue
          </h2>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center text-red-700 text-sm"
            >
              <AlertCircle className="w-4 h-4 mr-2 flex-shrink-0" />
              {error}
            </motion.div>
          )}

          {/* Google Sign-In Button */}
          <motion.button
            whileHover={{ scale: isLoading ? 1 : 1.02 }}
            whileTap={{ scale: isLoading ? 1 : 0.98 }}
            onClick={handleGoogleSignIn}
            disabled={isLoading}
            className={`w-full bg-white border-2 border-gray-200 rounded-lg px-4 py-3 flex items-center justify-center space-x-3 transition-all duration-200 ${
              isLoading
                ? 'cursor-not-allowed opacity-70'
                : 'hover:border-gray-300 hover:shadow-md'
            }`}
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin text-gray-600" />
            ) : (
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
            )}
            <span className="text-gray-700 font-medium">
              {isLoading ? 'Signing in...' : 'Continue with Google'}
            </span>
          </motion.button>
        </motion.div>

        {/* Medical Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="mt-8 pt-6 border-t border-gray-200"
        >
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <div className="flex items-start space-x-2">
              <Shield className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
              <div className="text-xs text-blue-700">
                <p className="font-medium mb-1">Healthcare Professional Use</p>
                <p className="leading-relaxed">
                  This platform is designed for medical professionals. 
                  AI analysis is for screening assistance only and should not replace clinical judgment.
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Privacy & Terms */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 1 }}
          className="text-xs text-gray-500 text-center mt-4 leading-relaxed"
        >
          By signing in, you agree to our Terms of Service and Privacy Policy. 
          All medical data is encrypted and HIPAA compliant.
        </motion.p>
      </motion.div>
    </div>
  );
};

export default GoogleSignIn;