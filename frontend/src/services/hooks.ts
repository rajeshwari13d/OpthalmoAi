import { useState, useEffect, useCallback } from 'react';
import { healthService, type HealthResponse } from '../services';

interface UseApiHealthReturn {
  isHealthy: boolean;
  isLoading: boolean;
  healthData: HealthResponse | null;
  error: string | null;
  checkHealth: () => Promise<void>;
}

/**
 * Hook to monitor API health status
 */
export const useApiHealth = (autoCheck = true, interval = 30000): UseApiHealthReturn => {
  const [isHealthy, setIsHealthy] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = useCallback(async () => {
    if (!autoCheck && isLoading) {
      setIsLoading(true);
    }

    try {
      const response = await healthService.checkHealth();
      
      if (response.success && response.data) {
        setIsHealthy(response.data.status === 'healthy');
        setHealthData(response.data);
        setError(null);
      } else {
        setIsHealthy(false);
        setHealthData(null);
        setError(response.error || 'Health check failed');
      }
    } catch (err) {
      setIsHealthy(false);
      setHealthData(null);
      setError(err instanceof Error ? err.message : 'Health check failed');
    } finally {
      setIsLoading(false);
    }
  }, [autoCheck, isLoading]);

  useEffect(() => {
    if (autoCheck) {
      // Initial health check
      checkHealth();

      // Set up periodic health checks
      const healthCheckInterval = setInterval(checkHealth, interval);

      return () => {
        clearInterval(healthCheckInterval);
      };
    }
  }, [autoCheck, interval, checkHealth]);

  return {
    isHealthy,
    isLoading,
    healthData,
    error,
    checkHealth,
  };
};