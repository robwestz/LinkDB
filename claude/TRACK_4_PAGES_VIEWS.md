# TRACK 4: Pages & Main Views [4/5]

**Agent:** Full-Stack Frontend Developer
**Status:** Ready to Execute (Wait for Track 1, 2, 3 to finish!)
**Credits:** Part of $150 budget (Claude Code)
**Estimated Time:** 3-4 hours

---

## 🎯 Mission

Du är **Track 4** i ett 5-track parallellt utvecklingsteam. Din uppgift är att bygga ALLA main pages/views som använder backend API och chart components.

**VIKTIGT:** Du är beroende av Track 1, 2, och 3. Vänta tills de är klara innan du börjar!

---

## 🚦 Boundary Rules

### ✅ DU FÅR RÖRA:
```
gui/frontend/src/pages/
├── Dashboard.jsx                   # Main dashboard
├── CustomerList.jsx                # Customer list view
├── CustomerAnalysis.jsx            # Customer deep dive (5 tabs!)
├── CompetitiveBenchmarking.jsx     # Competitive view
├── LinkExplorer.jsx                # Link browser/search
└── Settings.jsx                    # Settings page
```

### ❌ DU FÅR INTE RÖRA:
- `gui/frontend/src/components/layout/` - Track 2 gjorde detta
- `gui/frontend/src/components/common/` - Track 2 gjorde detta
- `gui/frontend/src/components/charts/` - Track 3 gjorde detta
- `gui/frontend/src/utils/` - Track 5 gör detta (men du behöver det!)
- `gui/backend/` - Track 1 gjorde detta

### ⚠️ DU FÅR IMPORTERA (men inte modifiera):
- Layout components från Track 2
- Common components från Track 2
- Chart components från Track 3
- API client från Track 5 (när det är klart)

---

## 👥 Dependencies på Andra Tracks

| Track | Vad du behöver från dem | Status Check |
|-------|-------------------------|--------------|
| **Track 1** | Backend API fungerande | Testa: `curl http://localhost:8000/health` |
| **Track 2** | Layout & common components | Testa: `npm run dev` ska visa sidebar |
| **Track 3** | Chart components | Importera: `import HealthGauge from '../components/charts/HealthGauge'` |
| **Track 5** | API client & hooks | Om inte klar: använd `fetch` direkt först |

**INNAN DU BÖRJAR:**
1. Verifiera Track 1 backend kör: `http://localhost:8000/api/customers`
2. Verifiera Track 2 layout fungerar
3. Verifiera Track 3 charts finns i `components/charts/`

---

## 📋 Din Uppgift

### Del 1: Dashboard Page (60 min)

**Fil:** `src/pages/Dashboard.jsx`

**Features:**
- KPI cards (Total Customers, Total Links, Avg Score)
- Customer health distribution chart
- Recent activity
- Top 10 performers table
- Alerts/warnings list

```jsx
import React, { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import LoadingSpinner from '../components/common/LoadingSpinner';
import HealthGauge from '../components/charts/HealthGauge';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch dashboard metrics från Track 1 API
    fetch('http://localhost:8000/api/dashboard/metrics')
      .then(res => res.json())
      .then(data => {
        setData(data.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching dashboard:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Customers</p>
              <p className="text-3xl font-bold">{data?.total_customers || 210}</p>
            </div>
            <div className="text-4xl">👥</div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Links</p>
              <p className="text-3xl font-bold">{data?.total_links || 4736}</p>
            </div>
            <div className="text-4xl">🔗</div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Average Health</p>
              <p className="text-3xl font-bold">{data?.avg_health || 75.2}</p>
            </div>
            <HealthGauge score={data?.avg_health || 75.2} size={80} />
          </div>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <Card title="Customer Health Distribution">
          {/* Add BarChart här från Track 3 */}
          <p className="text-gray-500">Health distribution chart</p>
        </Card>

        <Card title="Recent Activity">
          {/* Add LineChart här från Track 3 */}
          <p className="text-gray-500">Activity timeline</p>
        </Card>
      </div>

      {/* Top Performers & Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Top 10 Performers">
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2">Rank</th>
                  <th className="text-left py-2">Customer</th>
                  <th className="text-left py-2">Score</th>
                </tr>
              </thead>
              <tbody>
                {/* Populate från API */}
                <tr className="border-b">
                  <td className="py-2">1</td>
                  <td className="py-2">bethard.com</td>
                  <td className="py-2">80.1</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Card>

        <Card title="Alerts & Warnings">
          <div className="space-y-2">
            {/* Populate från API */}
            <div className="p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded">
              <p className="text-sm font-medium">⚠️ bethard.com: High over-optimization risk</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
```

### Del 2: Customer List Page (45 min)

**Fil:** `src/pages/CustomerList.jsx`

**Features:**
- Searchable/filterable customer table
- Click row to navigate to customer detail
- Sort by different columns
- Pagination

```jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Badge from '../components/common/Badge';
import LoadingSpinner from '../components/common/LoadingSpinner';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://localhost:8000/api/customers')
      .then(res => res.json())
      .then(data => {
        setCustomers(data.data || []);
        setLoading(false);
      });
  }, []);

  const filteredCustomers = customers.filter(c =>
    c.canonical_root?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <LoadingSpinner size="lg" />;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Customers</h1>

      {/* Search */}
      <Card className="mb-6">
        <input
          type="text"
          placeholder="Search customers..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </Card>

      {/* Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4">Customer</th>
                <th className="text-left py-3 px-4">Links</th>
                <th className="text-left py-3 px-4">Health Score</th>
                <th className="text-left py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredCustomers.map(customer => (
                <tr
                  key={customer.id}
                  onClick={() => navigate(`/customers/${customer.id}`)}
                  className="border-b hover:bg-gray-50 cursor-pointer"
                >
                  <td className="py-3 px-4 font-medium">{customer.canonical_root}</td>
                  <td className="py-3 px-4">{customer.total_links}</td>
                  <td className="py-3 px-4">{customer.health_score?.toFixed(1) || 'N/A'}</td>
                  <td className="py-3 px-4">
                    <Badge variant={customer.health_score >= 80 ? 'success' : 'warning'}>
                      {customer.health_score >= 80 ? 'Excellent' : 'Good'}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default CustomerList;
```

### Del 3: Customer Analysis Page - THE BIG ONE! (120+ min)

**Fil:** `src/pages/CustomerAnalysis.jsx`

**Features:**
- 5 TABS:
  1. Overview & Strategy
  2. Anchor Text Analysis
  3. Temporal Patterns
  4. Domain Quality
  5. Competitive Benchmarking

- Executive summary at top
- Each tab shows relevant charts + data

```jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Card from '../components/common/Card';
import Badge from '../components/common/Badge';
import LoadingSpinner from '../components/common/LoadingSpinner';
import HealthGauge from '../components/charts/HealthGauge';
import AnchorDistributionChart from '../components/charts/AnchorDistributionChart';
import TemporalChart from '../components/charts/TemporalChart';
import MonthlyDistributionChart from '../components/charts/MonthlyDistributionChart';
import DomainDistributionChart from '../components/charts/DomainDistributionChart';
import TLDDistributionChart from '../components/charts/TLDDistributionChart';

const CustomerAnalysis = () => {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    // Fetch comprehensive analysis från Track 1
    fetch(`http://localhost:8000/api/customers/${id}/analysis`)
      .then(res => res.json())
      .then(data => {
        setAnalysis(data.data);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <LoadingSpinner size="lg" />;
  if (!analysis) return <div>No data found</div>;

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
          <p className="text-2xl font-bold">{analysis.anchor_quality?.quality_score?.toFixed(1)}/100</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Temporal Health</p>
          <p className="text-2xl font-bold">{analysis.temporal_patterns?.health_score?.toFixed(1)}/100</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Domain Quality</p>
          <p className="text-2xl font-bold">{analysis.domain_quality?.quality_score?.toFixed(1)}/100</p>
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

          <Card title="Top 3 Priority Recommendations">
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

      {activeTab === 'anchor' && (
        <div className="space-y-6">
          <Card title="Anchor Quality Overview">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-sm text-gray-600">Quality Score</p>
                <p className="text-2xl font-bold">{analysis.anchor_quality?.quality_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Diversity</p>
                <p className="text-2xl font-bold">{analysis.anchor_quality?.diversity_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Exact Match %</p>
                <p className="text-2xl font-bold">{analysis.anchor_quality?.exact_match_ratio?.toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Risk</p>
                <Badge variant={analysis.anchor_quality?.over_optimization_risk === 'high' ? 'danger' : 'success'}>
                  {analysis.anchor_quality?.over_optimization_risk?.toUpperCase()}
                </Badge>
              </div>
            </div>

            <AnchorDistributionChart
              data={[
                { name: 'exact', value: analysis.anchor_quality?.exact_match_ratio || 0 },
                { name: 'branded', value: analysis.anchor_quality?.branded_ratio || 0 },
                { name: 'commercial', value: analysis.anchor_quality?.commercial_keywords_ratio || 0 },
              ]}
            />
          </Card>

          <Card title="Warnings">
            <div className="space-y-2">
              {analysis.anchor_quality?.warnings?.map((warning, i) => (
                <div key={i} className="p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded">
                  <p className="text-sm">{warning}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {activeTab === 'temporal' && (
        <div className="space-y-6">
          <Card title="Temporal Health">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-sm text-gray-600">Health Score</p>
                <p className="text-2xl font-bold">{analysis.temporal_patterns?.health_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Velocity</p>
                <p className="text-2xl font-bold">{analysis.temporal_patterns?.links_per_month?.toFixed(1)}/mo</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Trend</p>
                <Badge>{analysis.temporal_patterns?.velocity_trend?.toUpperCase()}</Badge>
              </div>
              <div>
                <p className="text-sm text-gray-600">Consistency</p>
                <p className="text-2xl font-bold">{analysis.temporal_patterns?.consistency_score?.toFixed(1)}/100</p>
              </div>
            </div>

            <MonthlyDistributionChart
              data={Object.entries(analysis.temporal_patterns?.monthly_distribution || {}).map(([month, count]) => ({
                month,
                count
              }))}
            />
          </Card>
        </div>
      )}

      {activeTab === 'domain' && (
        <div className="space-y-6">
          <Card title="Domain Quality">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-sm text-gray-600">Quality Score</p>
                <p className="text-2xl font-bold">{analysis.domain_quality?.quality_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Unique Domains</p>
                <p className="text-2xl font-bold">{analysis.domain_quality?.unique_domains}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Diversity</p>
                <p className="text-2xl font-bold">{analysis.domain_quality?.diversity_score?.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">PBN Risk</p>
                <p className="text-2xl font-bold">{analysis.domain_quality?.cross_linking_score?.toFixed(0)}/100</p>
              </div>
            </div>

            <TLDDistributionChart
              data={analysis.domain_quality?.top_tlds?.map(([tld, count]) => ({
                tld: `.${tld}`,
                count
              })) || []}
            />
          </Card>
        </div>
      )}

      {activeTab === 'competitive' && (
        <div>
          <Card title="Competitive Position">
            <p className="text-gray-600">Competitive data will be populated from API</p>
          </Card>
        </div>
      )}
    </div>
  );
};

export default CustomerAnalysis;
```

### Del 4: Competitive Benchmarking Page (45 min)

**Fil:** `src/pages/CompetitiveBenchmarking.jsx`

**Features:**
- Industry overview
- Top performers leaderboards
- Distribution charts
- Customer comparison table

```jsx
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

  if (loading) return <LoadingSpinner size="lg" />;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Competitive Benchmarking</h1>

      {/* Industry Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <Card>
          <p className="text-sm text-gray-600">Total Customers</p>
          <p className="text-2xl font-bold">{data?.total_customers || 210}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Avg Links/Customer</p>
          <p className="text-2xl font-bold">{data?.avg_total_links?.toFixed(1)}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Median Links</p>
          <p className="text-2xl font-bold">{data?.median_total_links?.toFixed(0)}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-600">Avg Quality</p>
          <p className="text-2xl font-bold">{data?.avg_quality?.toFixed(1)}</p>
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
            {data?.top_10_by_volume?.map(([domain, links], i) => (
              <div key={i} className="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
                <span className="font-medium">{i + 1}. {domain}</span>
                <span className="text-gray-600">{links} links</span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Top 10 by Quality">
          <div className="space-y-2">
            {data?.top_10_by_quality?.map(([domain, score], i) => (
              <div key={i} className="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
                <span className="font-medium">{i + 1}. {domain}</span>
                <span className="text-gray-600">{score.toFixed(1)}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default CompetitiveBenchmarking;
```

### Del 5: Link Explorer Page (60 min)

**Fil:** `src/pages/LinkExplorer.jsx`

**Features:**
- Searchable/filterable link table
- Pagination
- Expandable rows
- Bulk actions

```jsx
import React, { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import Badge from '../components/common/Badge';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';

const LinkExplorer = () => {
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({
    customer_id: null,
    anchor_type: null,
  });
  const [page, setPage] = useState(1);
  const limit = 50;

  useEffect(() => {
    const params = new URLSearchParams({
      offset: (page - 1) * limit,
      limit: limit,
      ...(search && { search }),
      ...(filters.customer_id && { customer_id: filters.customer_id }),
      ...(filters.anchor_type && { anchor_type: filters.anchor_type }),
    });

    fetch(`http://localhost:8000/api/links?${params}`)
      .then(res => res.json())
      .then(data => {
        setLinks(data.data || []);
        setLoading(false);
      });
  }, [page, search, filters]);

  if (loading) return <LoadingSpinner size="lg" />;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Link Explorer</h1>

      {/* Search & Filters */}
      <Card className="mb-6">
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Search links..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Button>Filter</Button>
          <Button variant="secondary">Export</Button>
        </div>
      </Card>

      {/* Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4">Customer</th>
                <th className="text-left py-3 px-4">Pub Domain</th>
                <th className="text-left py-3 px-4">Target URL</th>
                <th className="text-left py-3 px-4">Anchor Text</th>
                <th className="text-left py-3 px-4">Type</th>
                <th className="text-left py-3 px-4">Date</th>
              </tr>
            </thead>
            <tbody>
              {links.map((link, i) => (
                <tr key={i} className="border-b hover:bg-gray-50">
                  <td className="py-3 px-4">{link.customer}</td>
                  <td className="py-3 px-4">{link.pub_domain}</td>
                  <td className="py-3 px-4 truncate max-w-xs">{link.target_url}</td>
                  <td className="py-3 px-4">{link.anchor_text}</td>
                  <td className="py-3 px-4">
                    <Badge>{link.anchor_type}</Badge>
                  </td>
                  <td className="py-3 px-4">{link.published_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="mt-4 flex justify-between items-center">
          <p className="text-sm text-gray-600">
            Showing {(page - 1) * limit + 1}-{page * limit} of {links.length}
          </p>
          <div className="flex space-x-2">
            <Button variant="secondary" onClick={() => setPage(p => Math.max(1, p - 1))}>
              Previous
            </Button>
            <Button variant="secondary" onClick={() => setPage(p => p + 1)}>
              Next
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default LinkExplorer;
```

### Del 6: Settings Page (15 min)

**Fil:** `src/pages/Settings.jsx`

```jsx
import React from 'react';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const Settings = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Settings</h1>

      <Card title="Database Configuration">
        <p className="text-gray-600 mb-4">Database path and backup settings</p>
        <Button>Configure</Button>
      </Card>

      <Card title="Analysis Thresholds" className="mt-6">
        <p className="text-gray-600 mb-4">Customize warning thresholds</p>
        <Button>Edit Thresholds</Button>
      </Card>
    </div>
  );
};

export default Settings;
```

---

## 📊 Deliverables Checklist

- [ ] Dashboard page (KPIs + charts)
- [ ] Customer list page (table + search)
- [ ] Customer analysis page (5 tabs!)
- [ ] Competitive benchmarking page
- [ ] Link explorer page (filters + pagination)
- [ ] Settings page
- [ ] All pages integrated with Track 1 API
- [ ] All charts from Track 3 used
- [ ] Layout from Track 2 applied
- [ ] Loading states implemented
- [ ] Error handling
- [ ] Responsive design

---

## 🎯 Success Criteria

1. **All routes work**
2. **Data loads from backend API**
3. **Charts render with real data**
4. **Navigation between pages works**
5. **Loading spinners show during fetch**
6. **No console errors**

---

## 🔄 Update App.jsx

Replace placeholder pages in `App.jsx` med dina riktiga pages:

```jsx
import Dashboard from './pages/Dashboard';
import CustomerList from './pages/CustomerList';
import CustomerAnalysis from './pages/CustomerAnalysis';
import CompetitiveBenchmarking from './pages/CompetitiveBenchmarking';
import LinkExplorer from './pages/LinkExplorer';
import Settings from './pages/Settings';

// Replace routes...
<Route path="/" element={<Dashboard />} />
<Route path="/customers" element={<CustomerList />} />
<Route path="/customers/:id" element={<CustomerAnalysis />} />
// ... etc
```

---

## 🎬 Ready to Start?

1. **Wait for Track 1, 2, 3 to finish!**
2. **Open Claude Code**
3. **Load:** `TRACK_4_PAGES_VIEWS.md`
4. **Tell Claude Code:**
   ```
   Execute TRACK_4_PAGES_VIEWS.md

   You are Track 4 of 5 parallel tracks.
   Build ALL pages using components from Track 2 & 3.
   Integrate with backend API from Track 1.

   Create Dashboard, Customer pages, Competitive, Link Explorer.
   Customer Analysis page has 5 TABS - this is critical!

   Test each page as you build it.
   ```

**Track 4 skapar hela användargränssnittet!** 🖥️

*Estimated completion: 3-4 hours*
*Budget: ~$30-40 of $150 credits*
