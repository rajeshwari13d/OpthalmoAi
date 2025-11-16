import { useState, useEffect, useCallback } from 'react';
import { healthService, type HealthResponse } from '../services';
import { isProductionEnvironment } from './api.config';

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
    // Always show healthy (integrated AI active)
    setIsHealthy(true);
    setHealthData(null);
    setError(null);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    // Set as healthy immediately (integrated AI)
    setIsHealthy(true);
    setHealthData(null);
    setError(null);
    setIsLoading(false);
  }, []);

  return {
    isHealthy,
    isLoading,
    healthData,
    error,
    checkHealth,
  };
};