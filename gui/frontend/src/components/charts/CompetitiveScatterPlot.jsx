import React from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Label
} from 'recharts';

const CompetitiveScatterPlot = ({ data, currentCustomer }) => {
  // data format: [{ id: 117, domain: 'bethard.com', links: 56, quality: 80.1 }, ...]

  const avgLinks = data.reduce((sum, d) => sum + d.links, 0) / data.length;
  const avgQuality = data.reduce((sum, d) => sum + d.quality, 0) / data.length;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 rounded shadow-lg border border-gray-200">
          <p className="font-medium">{data.domain}</p>
          <p className="text-sm text-gray-600">Links: {data.links}</p>
          <p className="text-sm text-gray-600">Quality: {data.quality.toFixed(1)}</p>
        </div>
      );
    }
    return null;
  };

  const renderDot = (props) => {
    const { cx, cy, payload } = props;
    const isCurrent = payload.id === currentCustomer;

    return (
      <circle
        cx={cx}
        cy={cy}
        r={isCurrent ? 8 : 5}
        fill={isCurrent ? '#3b82f6' : '#9ca3af'}
        stroke={isCurrent ? '#1e40af' : 'none'}
        strokeWidth={isCurrent ? 2 : 0}
      />
    );
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          type="number"
          dataKey="links"
          name="Links"
          label={{ value: 'Total Links', position: 'insideBottom', offset: -5 }}
        />
        <YAxis
          type="number"
          dataKey="quality"
          name="Quality"
          label={{ value: 'Quality Score', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip content={<CustomTooltip />} />

        {/* Quadrant Lines */}
        <ReferenceLine x={avgLinks} stroke="#9ca3af" strokeDasharray="5 5" />
        <ReferenceLine y={avgQuality} stroke="#9ca3af" strokeDasharray="5 5" />

        <Scatter data={data} shape={renderDot} />
      </ScatterChart>
    </ResponsiveContainer>
  );
};

export default CompetitiveScatterPlot;
