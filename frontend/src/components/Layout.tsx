import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Eye, Shield, Stethoscope, Menu, X, Wifi, WifiOff, Home } from 'lucide-react';
import { Button, IconButton, Badge } from './ui';
import { useApiHealth } from '../services';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const { isHealthy, isLoading, healthData } = useApiHealth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (path: string) => {
    navigate(path);
    setMobileMenuOpen(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-teal-50/50">
      {/* Retinal Pattern Background */}
      <div className="fixed inset-0 opacity-30 pointer-events-none">
        <div className="absolute top-20 right-20 w-96 h-96 rounded-full bg-gradient-to-r from-teal-200/40 to-blue-200/40 blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 left-20 w-80 h-80 rounded-full bg-gradient-to-r from-emerald-200/40 to-teal-200/40 blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full border border-teal-200/30 opacity-50"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] rounded-full border border-blue-200/30 opacity-40"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[200px] h-[200px] rounded-full border border-emerald-200/30 opacity-30"></div>
      </div>

      {/* Navigation */}
      <nav className="relative bg-white/80 backdrop-blur-md border-b border-slate-200/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            {/* Logo - Make it clickable */}
            <div className="flex items-center space-x-3 cursor-pointer" onClick={() => handleNavigation('/')}>
              <div className="w-12 h-12 bg-white/10 backdrop-blur-sm rounded-xl shadow-lg flex items-center justify-center border border-white/20">
                <img 
                  src="/opthalmo-icon.svg" 
                  alt="OpthalmoAI" 
                  className="w-10 h-10 drop-shadow-sm"
                />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-teal-600 to-blue-600 bg-clip-text text-transparent">
                  OpthalmoAI
                </h1>
                <p className="text-sm text-slate-500 font-medium">AI-Powered Retinal Screening</p>
              </div>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-6">
              <nav className="flex space-x-1">
                <button 
                  onClick={() => handleNavigation('/')}
                  className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                    location.pathname === '/' 
                      ? 'text-teal-600 bg-teal-50' 
                      : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                  }`}
                >
                  <Home className="h-4 w-4 inline mr-2" />
                  Dashboard
                </button>
                <button 
                  onClick={() => handleNavigation('/upload')}
                  className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                    location.pathname === '/upload' || location.pathname === '/capture'
                      ? 'text-teal-600 bg-teal-50' 
                      : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                  }`}
                >
                  Screen
                </button>
                <button 
                  onClick={() => handleNavigation('/reports')}
                  className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                    location.pathname === '/reports' 
                      ? 'text-teal-600 bg-teal-50' 
                      : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                  }`}
                >
                  Reports
                </button>
                <button 
                  onClick={() => handleNavigation('/analytics')}
                  className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                    location.pathname === '/analytics' 
                      ? 'text-teal-600 bg-teal-50' 
                      : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                  }`}
                >
                  Analytics
                </button>
                <button 
                  onClick={() => handleNavigation('/home')}
                  className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                    location.pathname === '/home' 
                      ? 'text-teal-600 bg-teal-50' 
                      : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                  }`}
                >
                  About
                </button>
              </nav>
              <div className="flex items-center space-x-3">
                {/* API Health Indicator */}
                <div className="flex items-center space-x-2" title={healthData ? `API Status: ${healthData.status}` : 'Checking API...'}>
                  {isLoading ? (
                    <div className="animate-spin w-4 h-4 border-2 border-slate-300 border-t-teal-600 rounded-full"></div>
                  ) : isHealthy ? (
                    <Wifi className="h-4 w-4 text-emerald-600" />
                  ) : (
                    <WifiOff className="h-4 w-4 text-red-500" />
                  )}
                  <Badge variant={isHealthy ? 'success' : 'danger'} className="text-xs">
                    API {isHealthy ? 'Online' : 'Offline'}
                  </Badge>
                </div>
                
                <Button variant="outline" size="sm">
                  <Shield className="h-4 w-4 mr-2" />
                  HIPAA Compliant
                </Button>
              </div>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <IconButton
                icon={mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                variant="secondary"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              />
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-white/95 backdrop-blur-md border-t border-slate-200/50">
            <div className="px-4 py-4 space-y-2">
              <button 
                onClick={() => handleNavigation('/')}
                className={`flex items-center w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/' 
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                <Home className="h-4 w-4 mr-3" />
                Dashboard
              </button>
              <button 
                onClick={() => handleNavigation('/upload')}
                className={`block w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/upload' || location.pathname === '/capture'
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                Screen
              </button>
              <button 
                onClick={() => handleNavigation('/reports')}
                className={`block w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/reports' 
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                Reports
              </button>
              <button 
                onClick={() => handleNavigation('/analytics')}
                className={`block w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/analytics' 
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                Analytics
              </button>
              <button 
                onClick={() => handleNavigation('/home')}
                className={`block w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/home' 
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                About
              </button>
              <div className="pt-2">
                <Button variant="outline" size="sm" className="w-full">
                  <Shield className="h-4 w-4 mr-2" />
                  HIPAA Compliant
                </Button>
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main className="relative">
        {children}
      </main>

      {/* Footer */}
      <footer className="relative bg-white/60 backdrop-blur-sm border-t border-slate-200/50 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Company Info */}
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-teal-100 to-blue-100 rounded-lg shadow-sm flex items-center justify-center">
                  <img 
                    src="/opthalmo-icon.svg" 
                    alt="OpthalmoAI" 
                    className="w-8 h-8"
                  />
                </div>
                <h3 className="text-xl font-bold text-slate-800">OpthalmoAI</h3>
              </div>
              <p className="text-slate-600 text-sm leading-relaxed">
                AI-powered diabetic retinopathy screening platform designed to assist healthcare professionals 
                in early detection and patient care.
              </p>
            </div>

            {/* Medical Disclaimer */}
            <div>
              <h4 className="font-semibold text-slate-800 mb-4 flex items-center">
                <Stethoscope className="h-5 w-5 mr-2 text-teal-600" />
                Medical Notice
              </h4>
              <p className="text-slate-600 text-sm leading-relaxed">
                This platform is an assistive screening tool and <strong>not a substitute for professional medical diagnosis</strong>. 
                Always consult with qualified healthcare providers for proper medical evaluation.
              </p>
            </div>

            {/* Privacy & Security */}
            <div>
              <h4 className="font-semibold text-slate-800 mb-4 flex items-center">
                <Shield className="h-5 w-5 mr-2 text-teal-600" />
                Privacy & Security
              </h4>
              <ul className="text-slate-600 text-sm space-y-2">
                <li>• HIPAA-compliant data handling</li>
                <li>• Encrypted image processing</li>
                <li>• No permanent data storage</li>
                <li>• Secure, anonymized analysis</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-200/50 mt-8 pt-8 text-center">
            <p className="text-slate-500 text-sm">
              © 2025 OpthalmoAI. Healthcare AI technology for diabetic retinopathy screening. 
              <span className="text-teal-600 font-medium ml-2">Always consult your healthcare provider.</span>
            </p>
            <p className="text-slate-400 text-xs mt-2">
              Developed by <span className="font-medium text-teal-500">Pimpre</span>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;