import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

export const useCustomers = () => {
  return useQuery({
    queryKey: ['customers'],
    queryFn: () => api.getCustomers(),
  });
};

export const useCustomer = (customerId) => {
  return useQuery({
    queryKey: ['customer', customerId],
    queryFn: () => api.getCustomer(customerId),
    enabled: !!customerId,
  });
};
