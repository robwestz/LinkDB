import React, { useEffect, useState } from 'react';
import Card from '../common/Card';
import Badge from '../common/Badge';
import LoadingSpinner from '../common/LoadingSpinner';

const RecommendationsCard = ({ customerId }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!customerId) return;

    setLoading(true);
    fetch(`http://localhost:8000/api/ai/recommendations/${customerId}`)
      .then(res => res.json())
      .then(data => {
        setRecommendations(data.data.recommendations || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load recommendations:', err);
        setLoading(false);
      });
  }, [customerId]);

  if (loading) {
    return (
      <Card title="🎯 Smarta Rekommendationer">
        <div className="flex justify-center py-8">
          <LoadingSpinner size="lg" />
        </div>
      </Card>
    );
  }

  const impactColors = {
    high: 'danger',
    medium: 'warning',
    low: 'info',
  };

  return (
    <Card>
      <div className="flex items-center space-x-2 mb-4">
        <span className="text-2xl">🎯</span>
        <h3 className="text-lg font-semibold">Smarta Rekommendationer</h3>
      </div>

      <div className="space-y-4">
        {recommendations.map((rec, index) => (
          <div
            key={index}
            className="border-l-4 border-green-500 pl-4 py-3 bg-green-50 rounded-r"
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                  {rec.priority}
                </span>
                <h4 className="font-semibold text-gray-900">{rec.title}</h4>
              </div>
              <Badge variant={impactColors[rec.impact] || 'default'}>
                {(rec.impact || 'medium').toUpperCase()}
              </Badge>
            </div>

            <p className="text-sm text-gray-700 mb-2 ml-8">
              <strong className="text-green-700">Åtgärd:</strong> {rec.action}
            </p>

            <p className="text-xs text-gray-600 ml-8">
              <strong>Varför:</strong> {rec.reasoning}
            </p>
          </div>
        ))}

        {recommendations.length === 0 && (
          <p className="text-gray-500 text-center py-4">
            Inga rekommendationer tillgängliga.
          </p>
        )}
      </div>

      <div className="mt-4 pt-3 border-t border-gray-200 text-xs text-gray-500 text-center">
        🎯 AI-drivna rekommendationer • Uppdaterade för din profil
      </div>
    </Card>
  );
};

export default RecommendationsCard;
