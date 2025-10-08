import React from 'react';
import { motion } from 'framer-motion';
import { Eye, Activity, Brain } from 'lucide-react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary';
  text?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  variant = 'primary',
  text
}) => {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const colorClasses = {
    primary: 'text-teal-600',
    secondary: 'text-blue-600'
  };

  return (
    <div className="flex flex-col items-center space-y-3">
      <motion.div
        className={`${sizeClasses[size]} ${colorClasses[variant]}`}
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      >
        <svg className="w-full h-full" viewBox="0 0 24 24" fill="none">
          <circle
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeDasharray="60 20"
          />
        </svg>
      </motion.div>
      {text && (
        <motion.p
          className={`text-sm ${colorClasses[variant]} font-medium`}
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          {text}
        </motion.p>
      )}
    </div>
  );
};

export const AIProcessingLoader: React.FC = () => {
  const steps = [
    { icon: Eye, label: 'Analyzing Image', delay: 0 },
    { icon: Brain, label: 'AI Processing', delay: 0.5 },
    { icon: Activity, label: 'Generating Results', delay: 1 }
  ];

  return (
    <div className="flex items-center justify-center space-x-8">
      {steps.map((step, index) => {
        const IconComponent = step.icon;
        return (
          <motion.div
            key={index}
            className="flex flex-col items-center space-y-2"
            initial={{ opacity: 0.3, scale: 0.8 }}
            animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1, 0.8] }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: step.delay
            }}
          >
            <div className="w-12 h-12 bg-gradient-to-r from-teal-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
              <IconComponent className="h-6 w-6 text-white" />
            </div>
            <span className="text-sm text-slate-600 font-medium">
              {step.label}
            </span>
          </motion.div>
        );
      })}
    </div>
  );
};

interface ProgressRingProps {
  progress: number;
  size?: number;
  strokeWidth?: number;
  className?: string;
}

export const ProgressRing: React.FC<ProgressRingProps> = ({
  progress,
  size = 120,
  strokeWidth = 8,
  className = ''
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className={`relative ${className}`}>
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgb(226 232 240)"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        
        {/* Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="url(#progressGradient)"
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeLinecap="round"
          initial={{ strokeDasharray: circumference, strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />

        <defs>
          <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="rgb(20 184 166)" />
            <stop offset="100%" stopColor="rgb(59 130 246)" />
          </linearGradient>
        </defs>
      </svg>

      {/* Progress text */}
      <div className="absolute inset-0 flex items-center justify-center">
        <motion.span
          className="text-2xl font-bold bg-gradient-to-r from-teal-600 to-blue-600 bg-clip-text text-transparent"
          key={progress}
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          {Math.round(progress)}%
        </motion.span>
      </div>
    </div>
  );
};

export const RetinalScanAnimation: React.FC = () => {
  return (
    <div className="relative w-64 h-64">
      {/* Eye outline */}
      <svg
        className="absolute inset-0 w-full h-full"
        viewBox="0 0 256 256"
        fill="none"
      >
        <motion.path
          d="M128 64C192 64 224 128 224 128S192 192 128 192C64 192 32 128 32 128S64 64 128 64Z"
          stroke="rgb(20 184 166)"
          strokeWidth="3"
          fill="none"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2, ease: "easeInOut" }}
        />
        
        <motion.circle
          cx="128"
          cy="128"
          r="32"
          stroke="rgb(59 130 246)"
          strokeWidth="2"
          fill="none"
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{ duration: 1.5, delay: 0.5 }}
        />

        <motion.circle
          cx="128"
          cy="128"
          r="16"
          fill="rgb(16 185 129)"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5, delay: 1 }}
        />
      </svg>

      {/* Scanning lines */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-teal-400/30 to-transparent"
        initial={{ x: -256 }}
        animate={{ x: 256 }}
        transition={{
          duration: 2,
          repeat: Infinity,
          repeatDelay: 1,
          ease: "linear"
        }}
        style={{ width: '2px' }}
      />
    </div>
  );
};