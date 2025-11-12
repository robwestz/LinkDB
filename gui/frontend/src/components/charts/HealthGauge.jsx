import React from 'react';
import { PieChart, Pie, Cell } from 'recharts';

const HealthGauge = ({ score, label, size = 200 }) => {
  // Determine color based on score
  const getColor = (score) => {
    if (score >= 80) return '#10b981'; // green
    if (score >= 60) return '#f59e0b'; // yellow
    if (score >= 40) return '#f97316'; // orange
    return '#ef4444'; // red
  };

  const color = getColor(score);

  // Data for gauge (score + remaining to 100)
  const data = [
    { value: score },
    { value: 100 - score }
  ];

  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width: size, height: size }}>
        <PieChart width={size} height={size}>
          <Pie
            data={data}
            cx={size / 2}
            cy={size / 2}
            startAngle={180}
            endAngle={0}
            innerRadius={size * 0.6}
            outerRadius={size * 0.8}
            paddingAngle={0}
            dataKey="value"
          >
            <Cell fill={color} />
            <Cell fill="#e5e7eb" />
          </Pie>
        </PieChart>

        {/* Score Text Overlay */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-4xl font-bold" style={{ color }}>
            {score.toFixed(1)}
          </div>
          <div className="text-sm text-gray-600">/ 100</div>
        </div>
      </div>

      {label && (
        <div className="mt-2 text-sm font-medium text-gray-700">{label}</div>
      )}
    </div>
  );
};

export default HealthGauge;
