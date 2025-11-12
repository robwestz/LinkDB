import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Badge from '../components/common/Badge';
import LoadingSpinner from '../components/common/LoadingSpinner';
import EmptyState from '../components/common/EmptyState';
import { useCustomers } from '../hooks/useCustomers';
import useDebounce from '../hooks/useDebounce';
import { formatScore, getStatusFromScore } from '../utils/formatters';

const CustomerList = () => {
  const [search, setSearch] = useState('');
  const navigate = useNavigate();
  const debouncedSearch = useDebounce(search, 300);

  const { data: customers = [], isLoading, error } = useCustomers();

  const filteredCustomers = customers.filter(c =>
    c.canonical_root?.toLowerCase().includes(debouncedSearch.toLowerCase())
  );

  if (isLoading) return (
    <div className="flex items-center justify-center h-64">
      <LoadingSpinner size="lg" />
    </div>
  );

  if (error) {
    return <EmptyState message={`Error: ${error.message}`} icon="⚠️" />;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Customers</h1>

      {/* Search */}
      <Card className="mb-6">
        <input
          type="text"
          placeholder="Search customers..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </Card>

      {/* Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4">Customer</th>
                <th className="text-left py-3 px-4">Brand</th>
                <th className="text-left py-3 px-4">Links</th>
                <th className="text-left py-3 px-4">Health Score</th>
                <th className="text-left py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredCustomers.map(customer => (
                <tr
                  key={customer.id}
                  onClick={() => navigate(`/customers/${customer.id}`)}
                  className="border-b hover:bg-gray-50 cursor-pointer"
                >
                  <td className="py-3 px-4 font-medium">{customer.canonical_root}</td>
                  <td className="py-3 px-4">{customer.brand}</td>
                  <td className="py-3 px-4">{customer.total_links}</td>
                  <td className="py-3 px-4">{customer.health_score?.toFixed(1) || 'N/A'}</td>
                  <td className="py-3 px-4">
                    <Badge variant={customer.health_score >= 80 ? 'success' : 'warning'}>
                      {customer.health_score >= 80 ? 'Excellent' : 'Good'}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default CustomerList;
