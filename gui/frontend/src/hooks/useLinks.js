import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

export const useCustomerLinks = (customerId, offset = 0, limit = 50) => {
  return useQuery({
    queryKey: ['customerLinks', customerId, offset, limit],
    queryFn: () => api.getCustomerLinks(customerId, offset, limit),
    enabled: !!customerId,
  });
};

export const useLinks = (filters = {}, offset = 0, limit = 50) => {
  return useQuery({
    queryKey: ['links', filters, offset, limit],
    queryFn: () => api.getLinks({ ...filters, offset, limit }),
  });
};
