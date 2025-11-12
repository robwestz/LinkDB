import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const AnchorDistributionChart = ({ data }) => {
  // data format: [{ name: 'exact', value: 30 }, { name: 'partial', value: 40 }, ...]

  const COLORS = {
    exact: '#ef4444',      // red
    partial: '#f59e0b',    // yellow
    branded: '#3b82f6',    // blue
    generic: '#6b7280',    // gray
    lsi: '#8b5cf6',        // purple
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded shadow-lg border border-gray-200">
          <p className="font-medium">{payload[0].name}</p>
          <p className="text-sm text-gray-600">
            {payload[0].value.toFixed(1)}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#6b7280'} />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default AnchorDistributionChart;
