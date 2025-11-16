// OpthalmoAI API Config v2.0.1 - Build 20251116-2000
// Production and environment detection
export const isProductionEnvironment = (): boolean => {
  return process.env.NODE_ENV === 'production' ||
    (typeof window !== 'undefined' && 
     (window.location.hostname === 'opthalmoai.web.app' ||
      window.location.hostname.includes('firebase') ||
      window.location.hostname.includes('vercel') ||
      !window.location.hostname.includes('localhost')));
};

// API configuration and base URL
const getBaseUrl = (): string => {
  // Production or live site: no backend URLs to prevent network calls
  if (isProductionEnvironment()) {
    return '';
  }
  
  // Development environment only
  return process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
};

export const API_CONFIG = {
  BASE_URL: getBaseUrl(),
  API_VERSION: `/api/v1`, // API versioning for our server
  TIMEOUT: Number(process.env.REACT_APP_API_TIMEOUT) || 10000,
};

// API endpoints - empty in production to prevent network calls
export const API_ENDPOINTS = isProductionEnvironment() ? {} : {
  HEALTH: '/health',
  ANALYZE: '/analyze',
} as const;

// Build full API URL with versioning - returns empty string in production
export const buildApiUrl = (endpoint: string): string => {
  if (isProductionEnvironment()) {
    return '';
  }
  return `${API_CONFIG.BASE_URL}${API_CONFIG.API_VERSION}${endpoint}`;
};

// API Response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  version: string;
  uptime: number;
}

export interface AnalysisResult {
  id: string;
  stage: number;
  confidence: number;
  riskLevel: 'low' | 'moderate' | 'high';
  timestamp: string;
  recommendations: string[];
  processingTime?: number;
  imageUrl?: string;
  stageName?: string;
  imageQuality?: {
    qualityScore: number;
    brightness: number;
    contrast: number;
    sharpness?: number;
    fieldCoverage?: number;
    resolution?: string;
  };
  analysisDetails?: {
    fundusFeatures?: {
      microaneurysms: number;
      hemorrhages: number;
      exudates: number;
      cottonWoolSpots: number;
      neovascularization: boolean;
    };
    vesselsAnalysis?: {
      arteriovenousRatio: string;
      caliber: string;
      tortuosity: string;
    };
    macularAssessment?: {
      edemaPresent: boolean;
      fovealReflex: string;
      thickness: number;
    };
  };
  clinicalNotes?: string;
}

export interface AnalysisResponse {
  result: AnalysisResult;
  medical_disclaimer: string;
}

// API Error class
export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}