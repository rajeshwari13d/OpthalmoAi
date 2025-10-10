// API configuration and base URL
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000',
  API_VERSION: `/${process.env.REACT_APP_API_VERSION || 'v1'}`,
  TIMEOUT: Number(process.env.REACT_APP_API_TIMEOUT) || 30000,
};

export const API_ENDPOINTS = {
  HEALTH: '/health',
  ANALYZE: '/analyze',
} as const;

// Build full API URL
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
  service: string;
  version: string;
  timestamp: string;
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