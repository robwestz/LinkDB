import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis } from 'recharts';

const CompetitiveScatterPlot = ({ data, currentCustomer }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis type="number" dataKey="total_links" name="Total Links" />
        <YAxis type="number" dataKey="quality_score" name="Quality Score" />
        <ZAxis range={[60, 400]} />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter name="Customers" data={data} fill="#3b82f6" />
      </ScatterChart>
    </ResponsiveContainer>
  );
};

export default CompetitiveScatterPlot;
