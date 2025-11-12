import React, { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import Badge from '../components/common/Badge';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';

const LinkExplorer = () => {
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const limit = 50;

  useEffect(() => {
    const params = new URLSearchParams({
      offset: (page - 1) * limit,
      limit: limit,
      ...(search && { search }),
    });

    fetch(`http://localhost:8000/api/links?${params}`)
      .then(res => res.json())
      .then(data => {
        setLinks(data.data || []);
        setLoading(false);
      });
  }, [page, search]);

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <LoadingSpinner size="lg" />
    </div>
  );

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Link Explorer</h1>

      {/* Search & Filters */}
      <Card className="mb-6">
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Search links..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Button variant="secondary">Export</Button>
        </div>
      </Card>

      {/* Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4">Customer</th>
                <th className="text-left py-3 px-4">Pub Domain</th>
                <th className="text-left py-3 px-4">Target URL</th>
                <th className="text-left py-3 px-4">Anchor Text</th>
                <th className="text-left py-3 px-4">Type</th>
                <th className="text-left py-3 px-4">Date</th>
              </tr>
            </thead>
            <tbody>
              {links.map((link, i) => (
                <tr key={i} className="border-b hover:bg-gray-50">
                  <td className="py-3 px-4">{link.customer}</td>
                  <td className="py-3 px-4">{link.pub_domain}</td>
                  <td className="py-3 px-4 truncate max-w-xs">{link.target_url}</td>
                  <td className="py-3 px-4">{link.anchor_text}</td>
                  <td className="py-3 px-4">
                    <Badge>{link.anchor_type}</Badge>
                  </td>
                  <td className="py-3 px-4">{link.published_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="mt-4 flex justify-between items-center">
          <p className="text-sm text-gray-600">
            Showing {(page - 1) * limit + 1}-{Math.min(page * limit, links.length)} links
          </p>
          <div className="flex space-x-2">
            <Button
              variant="secondary"
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
            >
              Previous
            </Button>
            <Button
              variant="secondary"
              onClick={() => setPage(p => p + 1)}
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
