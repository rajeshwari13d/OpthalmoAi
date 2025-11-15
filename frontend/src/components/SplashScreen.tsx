import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Eye, Heart, Shield } from 'lucide-react';

interface SplashScreenProps {
  onComplete: () => void;
}

const SplashScreen: React.FC<SplashScreenProps> = ({ onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [loadingText, setLoadingText] = useState('Initializing...');

  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 2000);

    // Progress simulation
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 2.5;
      });
    }, 40);

    // Loading text updates
    const textTimer1 = setTimeout(() => setLoadingText('Loading AI Models...'), 600);
    const textTimer2 = setTimeout(() => setLoadingText('Preparing Healthcare Dashboard...'), 1200);
    const textTimer3 = setTimeout(() => setLoadingText('Almost Ready...'), 1800);

    return () => {
      clearTimeout(timer);
      clearInterval(progressInterval);
      clearTimeout(textTimer1);
      clearTimeout(textTimer2);
      clearTimeout(textTimer3);
    };
  }, [onComplete]);

  return (
    <div 
      className="fixed inset-0 flex items-center justify-center z-50"
      style={{
        background: `
          radial-gradient(circle at 20% 80%, rgba(13, 148, 136, 0.08) 0%, transparent 60%),
          radial-gradient(circle at 80% 20%, rgba(30, 58, 138, 0.08) 0%, transparent 60%),
          radial-gradient(circle at 40% 40%, rgba(15, 23, 42, 0.03) 0%, transparent 50%),
          linear-gradient(135deg, #0f172a 0%, #1e293b 15%, #334155 35%, #475569 60%, #64748b 85%, #94a3b8 100%)
        `
      }}
    >
      {/* Sophisticated Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Medical Grid Pattern */}
        <div 
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `
              radial-gradient(circle at center, #0D9488 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px'
          }}
        />
        
        {/* Neural Network Nodes */}
        <motion.div
          className="absolute top-1/4 left-1/5 w-2 h-2 rounded-full bg-teal-400/30"
          animate={{
            opacity: [0.2, 0.6, 0.2],
            scale: [1, 1.3, 1],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute top-1/3 right-1/4 w-1.5 h-1.5 rounded-full bg-blue-400/25"
          animate={{
            opacity: [0.15, 0.5, 0.15],
            scale: [1, 1.4, 1],
          }}
          transition={{
            duration: 3.5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 0.8,
          }}
        />
        <motion.div
          className="absolute bottom-1/3 left-1/2 w-2.5 h-2.5 rounded-full bg-teal-300/20"
          animate={{
            opacity: [0.1, 0.4, 0.1],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1.5,
          }}
        />
        
        {/* Subtle Connection Lines */}
        <svg className="absolute inset-0 w-full h-full opacity-10">
          <motion.path
            d="M 20% 25%, Q 50% 15%, 75% 33%"
            stroke="url(#gradient1)"
            strokeWidth="1"
            fill="none"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 0.3 }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          />
          <motion.path
            d="M 50% 67%, Q 70% 50%, 80% 25%"
            stroke="url(#gradient2)"
            strokeWidth="0.8"
            fill="none"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 0.25 }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 1 }}
          />
          <defs>
            <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#0D9488" stopOpacity="0.4" />
              <stop offset="100%" stopColor="transparent" />
            </linearGradient>
            <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#1E3A8A" stopOpacity="0.3" />
              <stop offset="100%" stopColor="transparent" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      {/* Main Content */}
      <div className="text-center z-10 max-w-md mx-auto px-6">
        {/* Sophisticated Logo Animation */}
        <motion.div
          initial={{ scale: 0, opacity: 0, rotateY: 180 }}
          animate={{ scale: 1, opacity: 1, rotateY: 0 }}
          transition={{ duration: 1.2, ease: "easeOut", type: "spring", stiffness: 100 }}
          className="mb-10"
        >
          <div className="relative mx-auto w-36 h-36 flex items-center justify-center">
            {/* Outer rotating ring - slower, elegant */}
            <motion.div
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="absolute inset-0 rounded-full border-2 opacity-30"
              style={{ 
                borderImage: 'linear-gradient(45deg, #0D9488, transparent, #1E3A8A, transparent) 1',
                borderColor: 'transparent'
              }}
            />
            
            {/* Middle counter-rotating ring */}
            <motion.div
              animate={{ rotate: [360, 0] }}
              transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
              className="absolute inset-3 rounded-full border opacity-20"
              style={{ 
                borderColor: '#64748b'
              }}
            />
            
            {/* Logo container with glass morphism */}
            <motion.div 
              className="w-24 h-24 rounded-full flex items-center justify-center backdrop-blur-sm border border-white/20"
              style={{ 
                background: `
                  linear-gradient(135deg, 
                    rgba(255, 255, 255, 0.25) 0%, 
                    rgba(255, 255, 255, 0.1) 50%, 
                    rgba(248, 250, 252, 0.15) 100%
                  )
                `,
                boxShadow: `
                  0 20px 40px -12px rgba(0, 0, 0, 0.25),
                  0 8px 32px rgba(13, 148, 136, 0.15),
                  inset 0 1px 0 rgba(255, 255, 255, 0.3),
                  inset 0 -1px 0 rgba(0, 0, 0, 0.1)
                `
              }}
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <img 
                src="/opthalmo-icon.svg" 
                alt="OpthalmoAI" 
                className="w-20 h-20 drop-shadow-lg"
              />
            </motion.div>
            
            {/* Subtle glow effect */}
            <div 
              className="absolute inset-6 rounded-full opacity-20 blur-sm"
              style={{ backgroundColor: '#0D9488' }}
            />
          </div>
        </motion.div>

        {/* Professional App Name */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1.0, delay: 0.4, ease: "easeOut" }}
          className="mb-8"
        >
          <motion.h1 
            className="text-5xl font-light text-white mb-3 tracking-wide"
            style={{ 
              textShadow: '0 2px 20px rgba(0, 0, 0, 0.3), 0 0 40px rgba(13, 148, 136, 0.2)',
              fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif'
            }}
            initial={{ letterSpacing: "0.2em", opacity: 0 }}
            animate={{ letterSpacing: "0.05em", opacity: 1 }}
            transition={{ duration: 1.5, delay: 0.6 }}
          >
            OpthalmoAI
          </motion.h1>
          <motion.p 
            className="text-slate-300 text-lg font-light tracking-wide"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            Advanced AI-Powered Retinal Analysis
          </motion.p>
          <motion.div
            className="w-20 h-px bg-gradient-to-r from-transparent via-teal-400/60 to-transparent mx-auto mt-4"
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ duration: 1.2, delay: 1.0 }}
          />
        </motion.div>

        {/* Professional Feature Icons */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1.0, delay: 0.8 }}
          className="flex justify-center space-x-12 mb-10"
        >
          <motion.div
            whileHover={{ scale: 1.05, y: -2 }}
            className="flex flex-col items-center text-slate-300 group"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.0 }}
          >
            <div 
              className="w-14 h-14 rounded-2xl flex items-center justify-center mb-3 backdrop-blur-sm border border-white/10 group-hover:border-teal-400/30 transition-all duration-300"
              style={{ 
                background: 'linear-gradient(135deg, rgba(13, 148, 136, 0.1), rgba(13, 148, 136, 0.05))',
                boxShadow: '0 8px 32px rgba(13, 148, 136, 0.1)'
              }}
            >
              <Eye className="w-7 h-7 text-teal-400/80" />
            </div>
            <span className="text-sm font-light tracking-wide">AI Vision</span>
          </motion.div>
          <motion.div
            whileHover={{ scale: 1.05, y: -2 }}
            className="flex flex-col items-center text-slate-300 group"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.2 }}
          >
            <div 
              className="w-14 h-14 rounded-2xl flex items-center justify-center mb-3 backdrop-blur-sm border border-white/10 group-hover:border-blue-400/30 transition-all duration-300"
              style={{ 
                background: 'linear-gradient(135deg, rgba(30, 58, 138, 0.15), rgba(30, 58, 138, 0.05))',
                boxShadow: '0 8px 32px rgba(30, 58, 138, 0.1)'
              }}
            >
              <Heart className="w-7 h-7 text-blue-400/80" />
            </div>
            <span className="text-sm font-light tracking-wide">Healthcare</span>
          </motion.div>
          <motion.div
            whileHover={{ scale: 1.05, y: -2 }}
            className="flex flex-col items-center text-slate-300 group"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.4 }}
          >
            <div 
              className="w-14 h-14 rounded-2xl flex items-center justify-center mb-3 backdrop-blur-sm border border-white/10 group-hover:border-teal-400/30 transition-all duration-300"
              style={{ 
                background: 'linear-gradient(135deg, rgba(13, 148, 136, 0.1), rgba(13, 148, 136, 0.05))',
                boxShadow: '0 8px 32px rgba(13, 148, 136, 0.1)'
              }}
            >
              <Shield className="w-7 h-7 text-teal-400/80" />
            </div>
            <span className="text-sm font-light tracking-wide">Secure</span>
          </motion.div>
        </motion.div>

        {/* Elegant Loading Progress */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1.0, delay: 1.2 }}
          className="w-full max-w-sm mx-auto"
        >
          <div className="flex items-center justify-between mb-4">
            <motion.span 
              className="text-slate-300 text-sm font-light tracking-wide"
              key={loadingText}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4 }}
            >
              {loadingText}
            </motion.span>
            <motion.span 
              className="text-slate-400 text-sm font-mono"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 1.4 }}
            >
              {Math.round(progress)}%
            </motion.span>
          </div>
          
          <div 
            className="w-full h-1 rounded-full overflow-hidden backdrop-blur-sm border border-white/10"
            style={{ 
              background: 'rgba(255, 255, 255, 0.05)'
            }}
          >
            <motion.div
              className="h-full rounded-full relative overflow-hidden"
              style={{ 
                background: 'linear-gradient(90deg, #0D9488 0%, #14B8A6 50%, #0D9488 100%)',
                boxShadow: '0 0 20px rgba(13, 148, 136, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2)'
              }}
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: `${progress}%`, opacity: 1 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
            >
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
                animate={{ x: ['-100%', '100%'] }}
                transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
                style={{ width: '50%' }}
              />
            </motion.div>
          </div>
        </motion.div>

        {/* Professional Medical Disclaimer */}
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1.6 }}
          className="text-slate-400 text-xs mt-8 leading-relaxed tracking-wide font-light max-w-xs mx-auto"
        >
          Enterprise-grade AI platform for professional healthcare screening
        </motion.p>
      </div>

      {/* Subtle Professional Footer */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.0, delay: 1.8 }}
      >
        <div className="flex items-center space-x-6 text-slate-500/60 text-xs">
          <motion.div
            animate={{ opacity: [0.3, 0.7, 0.3] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            className="flex items-center space-x-1"
          >
            <div className="w-1 h-1 bg-teal-400/60 rounded-full"></div>
            <span className="font-light tracking-wider">MEDICAL AI</span>
          </motion.div>
          <motion.div
            animate={{ opacity: [0.7, 0.3, 0.7] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 1 }}
            className="flex items-center space-x-1"
          >
            <div className="w-1 h-1 bg-blue-400/60 rounded-full"></div>
            <span className="font-light tracking-wider">HEALTHCARE</span>
          </motion.div>
          <motion.div
            animate={{ opacity: [0.3, 0.7, 0.3] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 2 }}
            className="flex items-center space-x-1"
          >
            <div className="w-1 h-1 bg-teal-400/60 rounded-full"></div>
            <span className="font-light tracking-wider">SECURE</span>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};

export default SplashScreen;