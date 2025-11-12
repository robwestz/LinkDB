import React, { useEffect, useState } from 'react';
import Card from '../common/Card';
import LoadingSpinner from '../common/LoadingSpinner';

const InsightsPanel = ({ customerId }) => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!customerId) return;

    setLoading(true);
    fetch(`http://localhost:8000/api/ai/insights/${customerId}`)
      .then(res => res.json())
      .then(data => {
        setInsights(data.data.insights || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load insights:', err);
        setLoading(false);
      });
  }, [customerId]);

  if (loading) {
    return (
      <Card title="🤖 AI-Genererade Insikter">
        <div className="flex justify-center py-8">
          <LoadingSpinner size="lg" />
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <div className="flex items-center space-x-2 mb-4">
        <span className="text-2xl">💡</span>
        <h3 className="text-lg font-semibold">AI-Genererade Insikter</h3>
      </div>

      <div className="space-y-3">
        {insights.map((insight, index) => (
          <div
            key={index}
            className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500"
          >
            <div className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
              {index + 1}
            </div>
            <p className="text-sm text-gray-800 flex-1">{insight}</p>
          </div>
        ))}

        {insights.length === 0 && (
          <p className="text-gray-500 text-center py-4">
            Inga insikter genererade än.
          </p>
        )}
      </div>

      <div className="mt-4 pt-3 border-t border-gray-200 text-xs text-gray-500 text-center">
        ✨ Genererat av AI • Uppdateras vid varje besök
      </div>
    </Card>
  );
};

export default InsightsPanel;
