import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

export const useCustomerAnalysis = (customerId) => {
  return useQuery({
    queryKey: ['analysis', customerId],
    queryFn: () => api.getCustomerAnalysis(customerId),
    enabled: !!customerId,
    staleTime: 2 * 60 * 1000, // 2 minutes (shorter for analysis)
  });
};
