import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, useLocation } from 'react-router-dom';
import { dataService } from '../services';
import { signOut } from 'firebase/auth';
import { auth } from '../config/firebase';
import { 
  Eye, 
  Upload, 
  FileText, 
  BarChart3, 
  LogOut, 
  Camera,
  Shield,
  Clock,
  ChevronRight,
  Activity,
  TrendingUp,
  Menu,
  X,
  Home,
  Stethoscope
} from 'lucide-react';

interface DashboardProps {
  user: any;
}

const Dashboard: React.FC<DashboardProps> = ({ user }) => {
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleSignOut = async () => {
    setIsLoggingOut(true);
    try {
      await signOut(auth);
    } catch (error) {
      console.error('Sign out error:', error);
    } finally {
      setIsLoggingOut(false);
    }
  };

  const refreshDashboardData = () => {
    setDashboardStats(dataService.getDashboardStats());
    setRecentActivities(dataService.getRecentActivities());
    setLastUpdated(new Date());
  };

  const quickActions = [
    {
      id: 'screen',
      title: 'AI Retinal Screening',
      description: 'Upload fundus images for diabetic retinopathy analysis',
      icon: Upload,
      color: 'from-medical-500 to-medical-600',
      action: () => navigate('/upload'),
      comingSoon: false
    },
    {
      id: 'camera',
      title: 'Capture Image',
      description: 'Direct eye photo scanning (Coming Soon)',
      icon: Camera,
      color: 'from-gray-400 to-gray-500',
      action: () => {},
      comingSoon: true
    },
    {
      id: 'reports',
      title: 'View Reports',
      description: 'Access patient analysis reports',
      icon: FileText,
      color: 'from-health-500 to-health-600',
      action: () => navigate('/reports')
    },
    {
      id: 'analytics',
      title: 'Analytics',
      description: 'View screening statistics',
      icon: BarChart3,
      color: 'from-purple-500 to-purple-600',
      action: () => navigate('/analytics')
    }
  ];

  const [dashboardStats, setDashboardStats] = useState(dataService.getDashboardStats());
  const [recentActivities, setRecentActivities] = useState(dataService.getRecentActivities());
  const [lastUpdated, setLastUpdated] = useState(new Date());

  // Check if user is new (created recently)
  const isNewUser = user?.metadata?.creationTime && 
    new Date().getTime() - new Date(user.metadata.creationTime).getTime() < 24 * 60 * 60 * 1000; // Less than 24 hours

  // Initialize sample data for new users and set up data refresh
  useEffect(() => {
    if (isNewUser && dashboardStats.totalScreenings === 0) {
      dataService.addSampleData();
      // Refresh data after adding sample data
      setDashboardStats(dataService.getDashboardStats());
      setRecentActivities(dataService.getRecentActivities());
      setLastUpdated(new Date());
    }
    
    // Update stats every 30 seconds
    const interval = setInterval(() => {
      setDashboardStats(dataService.getDashboardStats());
      setRecentActivities(dataService.getRecentActivities());
      setLastUpdated(new Date());
    }, 30000);

    // Refresh data when page becomes visible
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        refreshDashboardData();
      }
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      clearInterval(interval);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [isNewUser, dashboardStats.totalScreenings]);

  // Live stats based on actual data
  const recentStats = [
    { 
      label: 'Total Screenings', 
      value: dashboardStats.totalScreenings.toLocaleString(), 
      change: dashboardStats.weeklyChange.totalScreenings, 
      icon: Eye 
    },
    { 
      label: 'High Risk Cases', 
      value: dashboardStats.highRiskCases.toLocaleString(), 
      change: dashboardStats.weeklyChange.highRiskCases, 
      icon: Shield 
    },
    { 
      label: 'Reports Generated', 
      value: dashboardStats.reportsGenerated.toLocaleString(), 
      change: dashboardStats.weeklyChange.reportsGenerated, 
      icon: FileText 
    },
    { 
      label: 'This Week', 
      value: dashboardStats.thisWeekScreenings.toLocaleString(), 
      change: dashboardStats.weeklyChange.thisWeekScreenings, 
      icon: TrendingUp 
    }
  ];

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

      {/* Navigation Header */}
      <nav className="relative bg-white/80 backdrop-blur-md border-b border-slate-200/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            {/* Logo - Make it clickable */}
            <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
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
                  onClick={() => navigate('/')}
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
                  onClick={() => navigate('/upload')}
                  className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                    location.pathname === '/upload' 
                      ? 'text-teal-600 bg-teal-50' 
                      : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                  }`}
                >
                  Screen
                </button>
                <button 
                  onClick={() => navigate('/reports')}
                  className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                    location.pathname === '/reports' 
                      ? 'text-teal-600 bg-teal-50' 
                      : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                  }`}
                >
                  Reports
                </button>
                <button 
                  onClick={() => navigate('/analytics')}
                  className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                    location.pathname === '/analytics' 
                      ? 'text-teal-600 bg-teal-50' 
                      : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                  }`}
                >
                  Analytics
                </button>
                <button 
                  onClick={() => navigate('/home')}
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
                <div className="flex items-center space-x-2" title="AI Models Status">
                  <Activity className="h-4 w-4 text-emerald-600" />
                  <span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-1 rounded-full">
                    AI Online
                  </span>
                </div>
                
                {/* User Profile */}
                <div className="flex items-center space-x-3 border-l border-slate-200 pl-3">
                  {user?.photoURL && (
                    <img
                      src={user.photoURL}
                      alt={user.displayName}
                      className="w-8 h-8 rounded-full"
                    />
                  )}
                  <div className="text-right">
                    <p className="text-sm font-medium text-slate-900">
                      {user?.displayName}
                    </p>
                    <p className="text-xs text-slate-500">
                      Healthcare Professional
                    </p>
                  </div>
                  <button
                    onClick={handleSignOut}
                    disabled={isLoggingOut}
                    className="p-2 text-slate-400 hover:text-slate-600 transition-colors rounded-lg hover:bg-slate-100"
                    title="Sign Out"
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center space-x-2">
              {/* User Avatar on mobile */}
              {user?.photoURL && (
                <img
                  src={user.photoURL}
                  alt={user.displayName}
                  className="w-8 h-8 rounded-full"
                />
              )}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="p-2 text-slate-600 hover:text-slate-800 transition-colors"
              >
                {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-white/95 backdrop-blur-md border-t border-slate-200/50">
            <div className="px-4 py-4 space-y-2">
              <button 
                onClick={() => {
                  navigate('/');
                  setMobileMenuOpen(false);
                }}
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
                onClick={() => {
                  navigate('/upload');
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/upload' 
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                Screen
              </button>
              <button 
                onClick={() => {
                  navigate('/reports');
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/reports' 
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                Reports
              </button>
              <button 
                onClick={() => {
                  navigate('/analytics');
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/analytics' 
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                Analytics
              </button>
              <button 
                onClick={() => {
                  navigate('/home');
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                  location.pathname === '/home' 
                    ? 'text-teal-600 bg-teal-50' 
                    : 'text-slate-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
              >
                About
              </button>
              <div className="pt-2 border-t border-slate-200">
                <button
                  onClick={() => {
                    handleSignOut();
                    setMobileMenuOpen(false);
                  }}
                  disabled={isLoggingOut}
                  className="flex items-center w-full text-left px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition-all duration-200 font-medium"
                >
                  <LogOut className="h-4 w-4 mr-3" />
                  {isLoggingOut ? 'Signing Out...' : 'Sign Out'}
                </button>
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-8"
        >
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            {isNewUser ? `Welcome, ${user?.displayName?.split(' ')[0]}!` : `Welcome back, ${user?.displayName?.split(' ')[0]}`}
          </h2>
          <p className="text-gray-600">
            {isNewUser 
              ? 'Thank you for joining OpthalmoAI. Start your first diabetic retinopathy screening with AI-powered analysis.' 
              : 'Ready to continue diabetic retinopathy screening with AI-powered analysis.'
            }
          </p>
        </motion.div>

        {/* Quick Stats */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Statistics Overview</h2>
          <p className="text-xs text-gray-500">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </p>
        </div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          {recentStats.map((stat, index) => (
            <div key={stat.label} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <stat.icon className="w-8 h-8 text-medical-600" />
                <span className={`text-sm font-medium ${
                  stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'
                }`}>
                  {stat.change}
                </span>
              </div>
              <p className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</p>
              <p className="text-sm text-gray-600">{stat.label}</p>
            </div>
          ))}
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mb-8"
        >
          <h3 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {quickActions.map((action, index) => (
              <motion.button
                key={action.id}
                whileHover={action.comingSoon ? {} : { scale: 1.02, y: -2 }}
                whileTap={action.comingSoon ? {} : { scale: 0.98 }}
                onClick={action.comingSoon ? undefined : action.action}
                disabled={action.comingSoon}
                className={`bg-white rounded-xl p-6 shadow-sm border transition-all duration-200 text-left group ${
                  action.comingSoon 
                    ? 'border-gray-200 cursor-not-allowed opacity-75' 
                    : 'border-gray-200 hover:shadow-md cursor-pointer'
                }`}
              >
                <div className={`w-12 h-12 bg-gradient-to-r ${action.color} rounded-lg flex items-center justify-center mb-4 ${!action.comingSoon ? 'group-hover:scale-110' : ''} transition-transform duration-200`}>
                  <action.icon className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-semibold text-gray-900 mb-2">{action.title}</h4>
                <p className="text-sm text-gray-600 mb-3">{action.description}</p>
                <div className={`flex items-center text-sm font-medium ${
                  action.comingSoon ? 'text-gray-400' : 'text-medical-600'
                }`}>
                  <span>{action.comingSoon ? 'Coming Soon' : 'Get Started'}</span>
                  {!action.comingSoon && <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />}
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 gap-8">
          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
              <button
                onClick={refreshDashboardData}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
                title="Refresh activity"
              >
                <Activity className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-4">
              {recentActivities.length > 0 ? recentActivities.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <Clock className="w-4 h-4 text-gray-400 mt-1 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                    <p className="text-xs text-gray-600 mb-1">{activity.patient}</p>
                    <p className="text-xs text-gray-500">{activity.details}</p>
                    <p className="text-xs text-gray-400 mt-1">{activity.time}</p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium flex-shrink-0 ${
                    activity.risk.includes('No DR') ? 'bg-green-100 text-green-700' :
                    activity.risk.includes('Mild') ? 'bg-yellow-100 text-yellow-700' :
                    activity.risk.includes('Moderate') ? 'bg-orange-100 text-orange-700' :
                    activity.risk.includes('Severe') || activity.risk.includes('Proliferative') ? 'bg-red-100 text-red-700' :
                    'bg-blue-100 text-blue-700'
                  }`}>
                    {activity.risk}
                  </span>
                </div>
              )) : (
                <div className="text-center py-8 text-gray-500">
                  <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No recent activity</p>
                  <p className="text-xs text-gray-400 mt-1">Start analyzing retinal images to see activity here</p>
                </div>
              )}
            </div>
            <div className="mt-4 pt-4 border-t border-gray-200">
              <button 
                onClick={() => navigate('/reports')}
                className="text-sm text-teal-600 hover:text-teal-700 font-medium flex items-center"
              >
                View all activity
                <ChevronRight className="w-4 h-4 ml-1" />
              </button>
            </div>
          </motion.div>
        </div>

        {/* Medical Disclaimer */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-4"
        >
          <div className="flex items-start space-x-3">
            <Shield className="w-5 h-5 text-blue-600 mt-0.5" />
            <div className="text-sm text-blue-800">
              <p className="font-medium mb-1">Medical Disclaimer</p>
              <p className="leading-relaxed">
                OpthalmoAI provides AI-assisted screening for diabetic retinopathy. Results are for screening 
                purposes only and should not replace professional medical diagnosis. Always consult with 
                qualified healthcare professionals for medical decisions.
              </p>
            </div>
          </div>
        </motion.div>
      </div>

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

export default Dashboard;