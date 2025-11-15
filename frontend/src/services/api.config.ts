// API configuration and base URL
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8004',
  API_VERSION: `/api/v1`, // API versioning for our server
  TIMEOUT: Number(process.env.REACT_APP_API_TIMEOUT) || 30000,
};

export const API_ENDPOINTS = {
  HEALTH: '/health',
  ANALYZE: '/analyze',
} as const;

// Build full API URL with versioning
export const buildApiUrl = (endpoint: string): string => {
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
  };
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