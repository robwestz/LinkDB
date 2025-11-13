import React from 'react';
import HealthGauge from './HealthGauge';
import AnchorDistributionChart from './AnchorDistributionChart';
import TemporalChart from './TemporalChart';
import MonthlyDistributionChart from './MonthlyDistributionChart';
import DomainDistributionChart from './DomainDistributionChart';
import TLDDistributionChart from './TLDDistributionChart';
import CompetitiveScatterPlot from './CompetitiveScatterPlot';

/**
 * ChartsDemo - Test page showcasing all LinkDB chart components
 *
 * This component demonstrates all 7 chart types with sample data.
 * Use this as a reference for implementing charts in your pages.
 */

const ChartsDemo = () => {
  // Sample data for all charts
  const healthScore = 80.1;

  const anchorData = [
    { name: 'exact', value: 25 },
    { name: 'partial', value: 35 },
    { name: 'branded', value: 25 },
    { name: 'generic', value: 10 },
    { name: 'lsi', value: 5 },
  ];

  const temporalData = [
    { month: '2024-01', links: 45 },
    { month: '2024-02', links: 52 },
    { month: '2024-03', links: 48 },
    { month: '2024-04', links: 61 },
    { month: '2024-05', links: 55 },
    { month: '2024-06', links: 67 },
    { month: '2024-07', links: 63 },
    { month: '2024-08', links: 71 },
  ];

  const monthlyData = [
    { month: '2024-01', count: 45 },
    { month: '2024-02', count: 52 },
    { month: '2024-03', count: 68 },
    { month: '2024-04', count: 41 },
    { month: '2024-05', count: 35 },
    { month: '2024-06', count: 50 },
    { month: '2024-07', count: 58 },
    { month: '2024-08', count: 62 },
  ];

  const domainData = [
    { domain: 'bethard.com', count: 56 },
    { domain: 'casinostugan.com', count: 42 },
    { domain: 'mrgreen.se', count: 38 },
    { domain: 'leovegas.com', count: 35 },
    { domain: 'videoslots.com', count: 31 },
    { domain: 'casumo.com', count: 28 },
    { domain: 'rizk.com', count: 24 },
    { domain: 'casinoroom.com', count: 20 },
  ];

  const tldData = [
    { tld: '.se', count: 120 },
    { tld: '.com', count: 85 },
    { tld: '.org', count: 42 },
    { tld: '.net', count: 28 },
    { tld: '.io', count: 15 },
    { tld: '.co', count: 10 },
  ];

  const competitiveData = [
    { id: 117, domain: 'bethard.com', links: 56, quality: 80.1 },
    { id: 118, domain: 'casinostugan.com', links: 42, quality: 75.3 },
    { id: 119, domain: 'mrgreen.se', links: 68, quality: 82.5 },
    { id: 120, domain: 'leovegas.com', links: 51, quality: 78.9 },
    { id: 121, domain: 'videoslots.com', links: 39, quality: 71.2 },
    { id: 122, domain: 'casumo.com', links: 73, quality: 85.4 },
    { id: 123, domain: 'unibet.se', links: 45, quality: 69.8 },
    { id: 124, domain: 'paf.se', links: 62, quality: 77.6 },
  ];

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-4xl font-bold mb-8 text-gray-900">
        LinkDB Charts Demo
      </h1>
      <p className="text-lg text-gray-600 mb-12">
        Interactive data visualizations for LinkDB GUI - All 7 chart types
      </p>

      <div className="space-y-12">
        {/* Health Gauge */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            1. Health Gauge
          </h2>
          <p className="text-gray-600 mb-6">
            Circular gauge for scores 0-100 with color-coded zones
          </p>
          <div className="flex justify-center">
            <HealthGauge
              score={healthScore}
              label="Overall Link Health"
              size={200}
            />
          </div>
        </section>

        {/* Anchor Distribution */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            2. Anchor Distribution Chart
          </h2>
          <p className="text-gray-600 mb-6">
            Pie chart showing anchor text type distribution
          </p>
          <AnchorDistributionChart data={anchorData} />
        </section>

        {/* Temporal Chart - Line */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            3. Temporal Chart (Line)
          </h2>
          <p className="text-gray-600 mb-6">
            Line chart showing link acquisition over time
          </p>
          <TemporalChart data={temporalData} type="line" />
        </section>

        {/* Temporal Chart - Area */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            3b. Temporal Chart (Area)
          </h2>
          <p className="text-gray-600 mb-6">
            Area chart variant for temporal data
          </p>
          <TemporalChart data={temporalData} type="area" />
        </section>

        {/* Monthly Distribution */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            4. Monthly Distribution Chart
          </h2>
          <p className="text-gray-600 mb-6">
            Bar chart with best/worst month highlighting
          </p>
          <MonthlyDistributionChart
            data={monthlyData}
            bestMonth="2024-03"
            worstMonth="2024-05"
          />
        </section>

        {/* Domain Distribution */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            5. Domain Distribution Chart
          </h2>
          <p className="text-gray-600 mb-6">
            Horizontal bar chart for top domains
          </p>
          <DomainDistributionChart data={domainData} />
        </section>

        {/* TLD Distribution */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            6. TLD Distribution Chart
          </h2>
          <p className="text-gray-600 mb-6">
            Donut chart showing top-level domain distribution
          </p>
          <TLDDistributionChart data={tldData} />
        </section>

        {/* Competitive Scatter Plot */}
        <section className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            7. Competitive Scatter Plot
          </h2>
          <p className="text-gray-600 mb-6">
            Scatter plot with quadrants for competitive analysis
          </p>
          <CompetitiveScatterPlot
            data={competitiveData}
            currentCustomer={117}
          />
          <div className="mt-4 text-sm text-gray-600">
            <p>
              <strong>Blue dot (larger):</strong> Current customer (bethard.com)
            </p>
            <p>
              <strong>Gray dots:</strong> Competitors
            </p>
            <p>
              <strong>Quadrants:</strong> Divided by average links (vertical)
              and average quality (horizontal)
            </p>
          </div>
        </section>
      </div>

      {/* Footer */}
      <div className="mt-12 p-6 bg-blue-50 rounded-lg border border-blue-200">
        <h3 className="text-xl font-bold mb-2 text-blue-900">
          ✅ All Charts Ready!
        </h3>
        <p className="text-blue-700">
          All 7 chart components are fully functional and ready for integration.
          See README.md for detailed usage instructions.
        </p>
      </div>
    </div>
  );
};

export default ChartsDemo;
