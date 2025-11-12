import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

const MonthlyDistributionChart = ({ data, bestMonth, worstMonth }) => {
  // data format: [{ month: '2024-08', count: 5 }, ...]

  const getBarColor = (month) => {
    if (month === bestMonth) return '#10b981'; // green for best
    if (month === worstMonth) return '#ef4444'; // red for worst
    return '#3b82f6'; // blue default
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const isBest = payload[0].payload.month === bestMonth;
      const isWorst = payload[0].payload.month === worstMonth;

      return (
        <div className="bg-white p-3 rounded shadow-lg border border-gray-200">
          <p className="font-medium">{payload[0].payload.month}</p>
          <p className="text-sm text-gray-600">{payload[0].value} links</p>
          {isBest && <p className="text-xs text-green-600 mt-1">🏆 Best Month</p>}
          {isWorst && <p className="text-xs text-red-600 mt-1">⚠️ Worst Month</p>}
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" angle={-45} textAnchor="end" height={80} />
        <YAxis />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey="count" radius={[8, 8, 0, 0]}>
          {data.map((entry, index) => (
            <Cell key={`cell-${entry.month}`} fill={getBarColor(entry.month)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default MonthlyDistributionChart;
