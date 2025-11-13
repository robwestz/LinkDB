import React, { useState } from 'react';
import Card from '../components/common/Card';
import Badge from '../components/common/Badge';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import EmptyState from '../components/common/EmptyState';
import { useLinks } from '../hooks/useLinks';
import useDebounce from '../hooks/useDebounce';
import { exportToCSV, exportToJSON } from '../utils/export';
import { formatDate } from '../utils/formatters';

const LinkExplorer = () => {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const limit = 50;

  const debouncedSearch = useDebounce(search, 500);
  const {
    data: links = [],
    isLoading,
    error,
  } = useLinks({ search: debouncedSearch }, (page - 1) * limit, limit);

  const handleExportCSV = () => {
    exportToCSV(links, 'links-export.csv');
  };

  const handleExportJSON = () => {
    exportToJSON(links, 'links-export.json');
  };

  if (isLoading)
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );

  if (error) {
    return <EmptyState message={`Error: ${error.message}`} icon="⚠️" />;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
        Link Explorer
      </h1>

      {/* Search & Filters */}
      <Card className="mb-6">
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Search links..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-colors"
          />
          <div className="flex space-x-2">
            <Button variant="secondary" onClick={handleExportCSV}>
              Export CSV
            </Button>
            <Button variant="secondary" onClick={handleExportJSON}>
              Export JSON
            </Button>
          </div>
        </div>
      </Card>

      {/* Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300">
                  Customer
                </th>
                <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300">
                  Pub Domain
                </th>
                <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300">
                  Target URL
                </th>
                <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300">
                  Anchor Text
                </th>
                <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300">
                  Type
                </th>
                <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300">
                  Date
                </th>
              </tr>
            </thead>
            <tbody>
              {links.map((link, i) => (
                <tr
                  key={i}
                  className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <td className="py-3 px-4 text-gray-900 dark:text-gray-100">
                    {link.customer}
                  </td>
                  <td className="py-3 px-4 text-gray-700 dark:text-gray-300">
                    {link.pub_domain}
                  </td>
                  <td className="py-3 px-4 text-gray-700 dark:text-gray-300 truncate max-w-xs">
                    {link.target_url}
                  </td>
                  <td className="py-3 px-4 text-gray-700 dark:text-gray-300">
                    {link.anchor_text}
                  </td>
                  <td className="py-3 px-4">
                    <Badge>{link.anchor_type}</Badge>
                  </td>
                  <td className="py-3 px-4 text-gray-700 dark:text-gray-300">
                    {formatDate(link.published_at)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="mt-4 flex justify-between items-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Showing {(page - 1) * limit + 1}-
            {Math.min(page * limit, links.length)} links
          </p>
          <div className="flex space-x-2">
            <Button
              variant="secondary"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
            >
              Previous
            </Button>
            <Button
              variant="secondary"
              onClick={() => setPage((p) => p + 1)}
              disabled={links.length < limit}
            >
              Next
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default LinkExplorer;
