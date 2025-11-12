import React, { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import LoadingSpinner from '../components/common/LoadingSpinner';
import HealthGauge from '../components/charts/HealthGauge';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/dashboard/metrics')
      .then(res => res.json())
      .then(data => {
        setData(data.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching dashboard:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Customers</p>
              <p className="text-3xl font-bold">{data?.total_customers || 0}</p>
            </div>
            <div className="text-4xl">👥</div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Links</p>
              <p className="text-3xl font-bold">{data?.total_links || 0}</p>
            </div>
            <div className="text-4xl">🔗</div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Average Health</p>
              <p className="text-3xl font-bold">{data?.avg_health || 0}</p>
            </div>
            <HealthGauge score={data?.avg_health || 0} size={80} />
          </div>
        </Card>
      </div>

      {/* Top Performers */}
      <div className="grid grid-cols-1 gap-6">
        <Card title="Top Performers">
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2">Rank</th>
                  <th className="text-left py-2">Customer</th>
                  <th className="text-left py-2">Links</th>
                </tr>
              </thead>
              <tbody>
                {data?.top_performers?.map((performer, i) => (
                  <tr key={i} className="border-b hover:bg-gray-50">
                    <td className="py-2">{i + 1}</td>
                    <td className="py-2">{performer.domain}</td>
                    <td className="py-2">{performer.links}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
