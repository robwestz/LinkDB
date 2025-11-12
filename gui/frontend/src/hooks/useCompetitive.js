import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

export const useCompetitiveOverview = () => {
  return useQuery({
    queryKey: ['competitive', 'overview'],
    queryFn: () => api.getCompetitiveOverview(),
    staleTime: 10 * 60 * 1000, // 10 minutes (benchmarks change slowly)
  });
};

export const useCompetitiveComparison = (customerId) => {
  return useQuery({
    queryKey: ['competitive', 'comparison', customerId],
    queryFn: () => api.getCompetitiveComparison(customerId),
    enabled: !!customerId,
  });
};
