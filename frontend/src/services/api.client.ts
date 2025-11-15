import { 
  ApiResponse, 
  HealthResponse, 
  AnalysisResponse,
  AnalysisResult,
  ApiError,
  buildApiUrl,
  API_ENDPOINTS,
  API_CONFIG
} from './api.config';

/**
 * Base API client with error handling and request/response interceptors
 */
class ApiClient {
  private baseUrl: string;
  private timeout: number;

  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL;
    this.timeout = API_CONFIG.TIMEOUT;
  }

  /**
   * Generic request method with error handling
   */
  private async request<T>(
    url: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ 
          message: 'Unknown error occurred' 
        }));
        
        throw new ApiError(
          errorData.detail || errorData.message || `HTTP ${response.status}`,
          response.status,
          errorData.code
        );
      }

      const data = await response.json();
      return {
        success: true,
        data,
      };

    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof ApiError) {
        return {
          success: false,
          error: error.message,
        };
      }

      if (error instanceof DOMException && error.name === 'AbortError') {
        return {
          success: false,
          error: 'Request timeout - Analysis is taking longer than expected',
        };
      }

      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  /**
   * GET request
   */
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    const url = buildApiUrl(endpoint);
    return this.request<T>(url, { method: 'GET' });
  }

  /**
   * POST request with JSON body
   */
  async post<T>(endpoint: string, data: any): Promise<ApiResponse<T>> {
    const url = buildApiUrl(endpoint);
    return this.request<T>(url, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * POST request with FormData (for file uploads)
   */
  async postFormData<T>(endpoint: string, formData: FormData): Promise<ApiResponse<T>> {
    const url = buildApiUrl(endpoint);
    
    // Don't set Content-Type header for FormData - browser will set it with boundary
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ 
          message: 'Upload failed' 
        }));
        
        throw new ApiError(
          errorData.detail || errorData.message || `HTTP ${response.status}`,
          response.status,
          errorData.code
        );
      }

      const data = await response.json();
      return {
        success: true,
        data,
      };

    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof ApiError) {
        return {
          success: false,
          error: error.message,
        };
      }

      if (error instanceof DOMException && error.name === 'AbortError') {
        return {
          success: false,
          error: 'Upload timeout - Please try with a smaller image',
        };
      }

      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed',
      };
    }
  }
}

// Create singleton instance
export const apiClient = new ApiClient();

/**
 * Health check service
 */
export const healthService = {
  /**
   * Check API health status
   */
  async checkHealth(): Promise<ApiResponse<HealthResponse>> {
    return apiClient.get<HealthResponse>(API_ENDPOINTS.HEALTH);
  },

  /**
   * Ping the API to check if it's responding
   */
  async ping(): Promise<boolean> {
    try {
      const response = await healthService.checkHealth();
      return response.success && response.data?.status === 'healthy';
    } catch (error) {
      return false;
    }
  },
};

/**
 * Analysis service for retinal image processing
 */
export const analysisService = {
  /**
   * Analyze retinal fundus image for diabetic retinopathy
   */
  async analyzeImage(imageFile: File): Promise<ApiResponse<AnalysisResponse>> {
    // Validate file before sending
    const maxSizeMB = 10;
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];

    if (!allowedTypes.includes(imageFile.type)) {
      return {
        success: false,
        error: 'Invalid file type. Please upload a JPEG or PNG image.',
      };
    }

    if (imageFile.size > maxSizeMB * 1024 * 1024) {
      return {
        success: false,
        error: `File size too large. Maximum ${maxSizeMB}MB allowed.`,
      };
    }

    // Create FormData for file upload
    const formData = new FormData();
    formData.append('file', imageFile);

    return apiClient.postFormData<AnalysisResponse>(API_ENDPOINTS.ANALYZE, formData);
  },

  /**
   * Get analysis result by ID (placeholder for future implementation)
   */
  async getAnalysisResult(analysisId: string): Promise<ApiResponse<AnalysisResult>> {
    // TODO: Implement when backend supports result retrieval by ID
    return {
      success: false,
      error: 'Analysis result retrieval not yet implemented',
    };
  },
};