import React, { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import LoadingSpinner from '../components/common/LoadingSpinner';
import CompetitiveScatterPlot from '../components/charts/CompetitiveScatterPlot';

const CompetitiveBenchmarking = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/competitive/overview')
      .then(res => res.json())
      .then(data => {
        setData(data.data);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <LoadingSpinner size="lg" />
    </div>
  );

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Competitive Benchmarking</h1>

      {/* Industry Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <Card>
          <p className="text-sm text-gray-600">Total Customers</p>
          <p className="text-2xl font-bold">{data?.total_customers || 0}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Avg Links/Customer</p>
          <p className="text-2xl font-bold">{data?.avg_total_links?.toFixed(1) || 0}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Median Links</p>
          <p className="text-2xl font-bold">{data?.median_total_links?.toFixed(0) || 0}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Avg Quality</p>
          <p className="text-2xl font-bold">{data?.avg_quality?.toFixed(1) || 0}</p>
        </Card>
      </div>

      {/* Scatter Plot */}
      <Card title="Customer Distribution" className="mb-6">
        <CompetitiveScatterPlot
          data={data?.customers || []}
          currentCustomer={null}
        />
      </Card>

      {/* Leaderboards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Top 10 by Volume">
          <div className="space-y-2">
            {data?.top_10_by_volume?.map((item, i) => (
              <div key={i} className="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
                <span className="font-medium">{i + 1}. {item[0]}</span>
                <span className="text-gray-600">{item[1]} links</span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Top 10 by Quality">
          <div className="space-y-2">
            {data?.top_10_by_quality?.map((item, i) => (
              <div key={i} className="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
                <span className="font-medium">{i + 1}. {item[0]}</span>
                <span className="text-gray-600">{typeof item[1] === 'number' ? item[1].toFixed(1) : item[1]}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default CompetitiveBenchmarking;
