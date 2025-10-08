import React from 'react';
import { motion } from 'framer-motion';

interface AnimatedCardProps {
  children: React.ReactNode;
  delay?: number;
  className?: string;
}

export const AnimatedCard: React.FC<AnimatedCardProps> = ({ 
  children, 
  delay = 0, 
  className = '' 
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay }}
      whileHover={{ y: -5, scale: 1.02 }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

interface FloatingElementProps {
  children: React.ReactNode;
  direction?: 'up' | 'down';
  duration?: number;
}

export const FloatingElement: React.FC<FloatingElementProps> = ({ 
  children, 
  direction = 'up',
  duration = 3 
}) => {
  return (
    <motion.div
      animate={{ 
        y: direction === 'up' ? [-10, 10, -10] : [10, -10, 10] 
      }}
      transition={{ 
        duration, 
        repeat: Infinity, 
        ease: "easeInOut" 
      }}
    >
      {children}
    </motion.div>
  );
};

export const RetinalPattern: React.FC = () => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Animated gradient orbs */}
      <motion.div
        className="absolute top-20 right-20 w-96 h-96 rounded-full bg-gradient-to-r from-teal-200/40 to-blue-200/40 blur-3xl"
        animate={{ 
          scale: [1, 1.2, 1],
          rotate: [0, 90, 180, 270, 360]
        }}
        transition={{ 
          duration: 20,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      
      <motion.div
        className="absolute bottom-20 left-20 w-80 h-80 rounded-full bg-gradient-to-r from-emerald-200/40 to-teal-200/40 blur-3xl"
        animate={{ 
          scale: [1.2, 1, 1.2],
          rotate: [360, 270, 180, 90, 0]
        }}
        transition={{ 
          duration: 15,
          repeat: Infinity,
          ease: "linear"
        }}
      />

      {/* Retinal vessel pattern */}
      <svg 
        className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] opacity-20"
        viewBox="0 0 800 800"
      >
        <motion.circle
          cx="400"
          cy="400"
          r="300"
          fill="none"
          stroke="url(#gradient1)"
          strokeWidth="2"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 3, ease: "easeInOut" }}
        />
        
        <motion.circle
          cx="400"
          cy="400"
          r="200"
          fill="none"
          stroke="url(#gradient2)"
          strokeWidth="1.5"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2.5, delay: 0.5, ease: "easeInOut" }}
        />
        
        <motion.circle
          cx="400"
          cy="400"
          r="100"
          fill="none"
          stroke="url(#gradient3)"
          strokeWidth="1"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2, delay: 1, ease: "easeInOut" }}
        />

        <defs>
          <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="rgb(20 184 166)" stopOpacity="0.3" />
            <stop offset="50%" stopColor="rgb(59 130 246)" stopOpacity="0.3" />
            <stop offset="100%" stopColor="rgb(16 185 129)" stopOpacity="0.3" />
          </linearGradient>
          
          <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="rgb(59 130 246)" stopOpacity="0.4" />
            <stop offset="100%" stopColor="rgb(20 184 166)" stopOpacity="0.4" />
          </linearGradient>
          
          <linearGradient id="gradient3" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="rgb(16 185 129)" stopOpacity="0.5" />
            <stop offset="100%" stopColor="rgb(59 130 246)" stopOpacity="0.5" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
};

interface PulseIndicatorProps {
  size?: 'sm' | 'md' | 'lg';
  color?: 'teal' | 'blue' | 'emerald';
}

export const PulseIndicator: React.FC<PulseIndicatorProps> = ({ 
  size = 'md', 
  color = 'teal' 
}) => {
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3', 
    lg: 'w-4 h-4'
  };

  const colorClasses = {
    teal: 'bg-teal-400',
    blue: 'bg-blue-400',
    emerald: 'bg-emerald-400'
  };

  return (
    <div className="relative">
      <motion.div
        className={`${sizeClasses[size]} ${colorClasses[color]} rounded-full`}
        animate={{ scale: [1, 1.5, 1] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
      <motion.div
        className={`absolute inset-0 ${sizeClasses[size]} ${colorClasses[color]} rounded-full opacity-40`}
        animate={{ scale: [1, 2, 1], opacity: [0.4, 0, 0.4] }}
        transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
      />
    </div>
  );
};