import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import Card from '../components/common/Card';
import Badge from '../components/common/Badge';
import LoadingSpinner from '../components/common/LoadingSpinner';
import EmptyState from '../components/common/EmptyState';
import HealthGauge from '../components/charts/HealthGauge';
import AnchorDistributionChart from '../components/charts/AnchorDistributionChart';
import MonthlyDistributionChart from '../components/charts/MonthlyDistributionChart';
import TLDDistributionChart from '../components/charts/TLDDistributionChart';
import { useCustomerAnalysis } from '../hooks/useAnalysis';

const CustomerAnalysis = () => {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState('overview');

  const { data: analysis, isLoading, error } = useCustomerAnalysis(id);

  if (isLoading) return (
    <div className="flex items-center justify-center h-64">
      <LoadingSpinner size="lg" />
    </div>
  );

  if (error || !analysis) return (
    <EmptyState
      message={error?.message || 'Analysis not available'}
      icon="📊"
    />
  );

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'anchor', label: 'Anchor Analysis' },
    { id: 'temporal', label: 'Temporal Patterns' },
    { id: 'domain', label: 'Domain Quality' },
    { id: 'competitive', label: 'Competitive' },
  ];

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold">{analysis.canonical_root}</h1>
        <p className="text-gray-600">{analysis.brand}</p>
      </div>

      {/* Executive Summary */}
      <Card className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold mb-2">Overall Health</h2>
            <p className="text-lg">
              <Badge variant={analysis.overall_score >= 80 ? 'success' : 'warning'}>
                {analysis.overall_score >= 80 ? 'EXCELLENT' : 'GOOD'}
              </Badge>
            </p>
          </div>
          <HealthGauge score={analysis.overall_score} size={150} />
        </div>
      </Card>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <Card>
          <p className="text-sm text-gray-600">Anchor Quality</p>
          <p className="text-2xl font-bold">
            {analysis.anchor_quality?.quality_score?.toFixed(1) || 'N/A'}/100
          </p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Temporal Health</p>
          <p className="text-2xl font-bold">
            {analysis.temporal_patterns?.health_score?.toFixed(1) || 'N/A'}/100
          </p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Domain Quality</p>
          <p className="text-2xl font-bold">
            {analysis.domain_quality?.quality_score?.toFixed(1) || 'N/A'}/100
          </p>
        </Card>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <div className="flex space-x-8">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-2 border-b-2 font-medium transition-colors ${
                activeTab === tab.id
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <Card title="Link Portfolio">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-600">Total Links</p>
                <p className="text-2xl font-bold">{analysis.link_history?.total_links}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Unique Domains</p>
                <p className="text-2xl font-bold">{analysis.link_history?.unique_pub_domains}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Target URLs</p>
                <p className="text-2xl font-bold">{analysis.link_history?.unique_target_urls}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Links/Month</p>
                <p className="text-2xl font-bold">{analysis.link_history?.links_per_month?.toFixed(1)}</p>
              </div>
            </div>
          </Card>

          <Card title="Top Recommendations">
            <div className="space-y-3">
              {analysis.link_history?.recommendations?.slice(0, 3).map((rec, i) => (
                <div key={i} className="p-3 bg-gray-50 rounded-lg">
                  <p>{rec}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {activeTab === 'anchor' && analysis.anchor_quality && (
        <div className="space-y-6">
          <Card title="Anchor Quality Overview">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-sm text-gray-600">Quality Score</p>
                <p className="text-2xl font-bold">{analysis.anchor_quality.quality_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Diversity</p>
                <p className="text-2xl font-bold">{analysis.anchor_quality.diversity_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Exact Match %</p>
                <p className="text-2xl font-bold">{analysis.anchor_quality.exact_match_ratio?.toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Risk</p>
                <Badge variant={analysis.anchor_quality.over_optimization_risk === 'high' ? 'danger' : 'success'}>
                  {analysis.anchor_quality.over_optimization_risk?.toUpperCase()}
                </Badge>
              </div>
            </div>

            <AnchorDistributionChart
              data={[
                { name: 'Exact Match', value: analysis.anchor_quality.exact_match_ratio || 0 },
                { name: 'Branded', value: analysis.anchor_quality.branded_ratio || 0 },
                { name: 'Commercial', value: analysis.anchor_quality.commercial_keywords_ratio || 0 },
              ]}
            />
          </Card>

          {analysis.anchor_quality.warnings && analysis.anchor_quality.warnings.length > 0 && (
            <Card title="Warnings">
              <div className="space-y-2">
                {analysis.anchor_quality.warnings.map((warning, i) => (
                  <div key={i} className="p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded">
                    <p className="text-sm">{warning}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}

      {activeTab === 'temporal' && analysis.temporal_patterns && (
        <div className="space-y-6">
          <Card title="Temporal Health">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-sm text-gray-600">Health Score</p>
                <p className="text-2xl font-bold">{analysis.temporal_patterns.health_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Velocity</p>
                <p className="text-2xl font-bold">{analysis.temporal_patterns.links_per_month?.toFixed(1)}/mo</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Trend</p>
                <Badge>{analysis.temporal_patterns.velocity_trend?.toUpperCase()}</Badge>
              </div>
              <div>
                <p className="text-sm text-gray-600">Consistency</p>
                <p className="text-2xl font-bold">{analysis.temporal_patterns.consistency_score?.toFixed(1)}/100</p>
              </div>
            </div>

            <MonthlyDistributionChart
              data={Object.entries(analysis.temporal_patterns.monthly_distribution || {}).map(([month, count]) => ({
                month,
                count
              }))}
            />
          </Card>
        </div>
      )}

      {activeTab === 'domain' && analysis.domain_quality && (
        <div className="space-y-6">
          <Card title="Domain Quality">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-sm text-gray-600">Quality Score</p>
                <p className="text-2xl font-bold">{analysis.domain_quality.quality_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Unique Domains</p>
                <p className="text-2xl font-bold">{analysis.domain_quality.unique_domains}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Diversity</p>
                <p className="text-2xl font-bold">{analysis.domain_quality.diversity_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Cross-linking</p>
                <p className="text-2xl font-bold">{analysis.domain_quality.cross_linking_score?.toFixed(0)}/100</p>
              </div>
            </div>

            {analysis.domain_quality.top_tlds && (
              <TLDDistributionChart
                data={analysis.domain_quality.top_tlds.map(([tld, count]) => ({
                  tld: `.${tld}`,
                  count
                }))}
              />
            )}
          </Card>
        </div>
      )}

      {activeTab === 'competitive' && (
        <div>
          <Card title="Competitive Position">
            <p className="text-gray-600">Competitive analysis coming soon...</p>
          </Card>
        </div>
      )}
    </div>
  );
};

export default CustomerAnalysis;
