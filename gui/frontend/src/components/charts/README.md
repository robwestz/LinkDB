# Chart Components - LinkDB GUI

Beautiful, interactive, and responsive data visualizations built with Recharts for the LinkDB GUI application.

## 📦 Installation

All dependencies are already installed. Charts use:
- **Recharts** - React charting library
- **React** - UI framework
- **Tailwind CSS** - Styling (for tooltips and layout)

## 🎨 Available Charts

### 1. HealthGauge

Circular gauge for displaying scores from 0-100 with color-coded zones.

**Props:**
- `score` (number, required): Score value 0-100
- `label` (string, optional): Label displayed below the gauge
- `size` (number, optional, default: 200): Size in pixels

**Color Zones:**
- 🟢 Green (80-100): Excellent
- 🟡 Yellow (60-79): Good
- 🟠 Orange (40-59): Fair
- 🔴 Red (0-39): Poor

**Usage:**
```jsx
import { HealthGauge } from './components/charts';

<HealthGauge
  score={80.1}
  label="Overall Health"
  size={200}
/>
```

**Sample Data:**
```jsx
const score = 75.3;
```

---

### 2. AnchorDistributionChart

Pie chart showing the distribution of anchor text types.

**Props:**
- `data` (array, required): Array of anchor type distribution

**Data Format:**
```javascript
[
  { name: 'exact', value: 30 },
  { name: 'partial', value: 40 },
  { name: 'branded', value: 20 },
  { name: 'generic', value: 10 }
]
```

**Anchor Types & Colors:**
- `exact` - 🔴 Red (#ef4444)
- `partial` - 🟡 Yellow (#f59e0b)
- `branded` - 🔵 Blue (#3b82f6)
- `generic` - ⚪ Gray (#6b7280)
- `lsi` - 🟣 Purple (#8b5cf6)

**Usage:**
```jsx
import { AnchorDistributionChart } from './components/charts';

const anchorData = [
  { name: 'exact', value: 25 },
  { name: 'partial', value: 35 },
  { name: 'branded', value: 25 },
  { name: 'generic', value: 10 },
  { name: 'lsi', value: 5 }
];

<AnchorDistributionChart data={anchorData} />
```

**Features:**
- Interactive tooltips with percentages
- Legend with color coding
- Responsive container

---

### 3. TemporalChart

Line or area chart for displaying temporal patterns over time.

**Props:**
- `data` (array, required): Array of temporal data points
- `type` (string, optional, default: 'line'): Chart type ('line' or 'area')

**Data Format:**
```javascript
[
  { month: '2024-08', links: 5 },
  { month: '2024-09', links: 8 },
  { month: '2024-10', links: 12 }
]
```

**Usage:**
```jsx
import { TemporalChart } from './components/charts';

const temporalData = [
  { month: '2024-01', links: 45 },
  { month: '2024-02', links: 52 },
  { month: '2024-03', links: 48 },
  { month: '2024-04', links: 61 },
  { month: '2024-05', links: 55 },
  { month: '2024-06', links: 67 }
];

// Line chart
<TemporalChart data={temporalData} type="line" />

// Area chart
<TemporalChart data={temporalData} type="area" />
```

**Features:**
- Smooth monotone curves
- Interactive hover with active dots
- Gridlines for easy reading
- Legend and axis labels

---

### 4. MonthlyDistributionChart

Bar chart showing monthly distribution with highlighting for best/worst months.

**Props:**
- `data` (array, required): Array of monthly data
- `bestMonth` (string, optional): Month identifier to highlight as best
- `worstMonth` (string, optional): Month identifier to highlight as worst

**Data Format:**
```javascript
[
  { month: '2024-08', count: 5 },
  { month: '2024-09', count: 8 },
  { month: '2024-10', count: 12 }
]
```

**Usage:**
```jsx
import { MonthlyDistributionChart } from './components/charts';

const monthlyData = [
  { month: '2024-01', count: 45 },
  { month: '2024-02', count: 52 },
  { month: '2024-03', count: 68 },  // Best
  { month: '2024-04', count: 41 },
  { month: '2024-05', count: 35 },  // Worst
  { month: '2024-06', count: 50 }
];

<MonthlyDistributionChart
  data={monthlyData}
  bestMonth="2024-03"
  worstMonth="2024-05"
/>
```

**Features:**
- Color-coded bars:
  - 🟢 Green for best month
  - 🔴 Red for worst month
  - 🔵 Blue for other months
- Angled X-axis labels for readability
- Tooltips with special annotations

---

### 5. DomainDistributionChart

Horizontal bar chart showing top domains by link count.

**Props:**
- `data` (array, required): Array of domain statistics

**Data Format:**
```javascript
[
  { domain: 'example.com', count: 25 },
  { domain: 'test.se', count: 18 },
  { domain: 'site.org', count: 15 }
]
```

**Usage:**
```jsx
import { DomainDistributionChart } from './components/charts';

const domainData = [
  { domain: 'bethard.com', count: 56 },
  { domain: 'casinostugan.com', count: 42 },
  { domain: 'mrgreen.se', count: 38 },
  { domain: 'leovegas.com', count: 35 },
  { domain: 'videoslots.com', count: 31 },
  { domain: 'casumo.com', count: 28 },
  { domain: 'rizk.com', count: 24 },
  { domain: 'casinoroom.com', count: 20 }
];

<DomainDistributionChart data={domainData} />
```

**Features:**
- Horizontal layout for long domain names
- Rounded bar edges
- Interactive tooltips
- Responsive height (400px)

---

### 6. TLDDistributionChart

Donut chart showing distribution of top-level domains.

**Props:**
- `data` (array, required): Array of TLD statistics

**Data Format:**
```javascript
[
  { tld: '.se', count: 45 },
  { tld: '.com', count: 38 },
  { tld: '.org', count: 12 }
]
```

**Usage:**
```jsx
import { TLDDistributionChart } from './components/charts';

const tldData = [
  { tld: '.se', count: 120 },
  { tld: '.com', count: 85 },
  { tld: '.org', count: 42 },
  { tld: '.net', count: 28 },
  { tld: '.io', count: 15 },
  { tld: '.co', count: 10 }
];

<TLDDistributionChart data={tldData} />
```

**Features:**
- Donut style (inner + outer radius)
- Color palette: blue, purple, pink, orange, green, gray
- Labels with percentages
- Legend and interactive tooltips

---

### 7. CompetitiveScatterPlot

Scatter plot with quadrants for competitive analysis.

**Props:**
- `data` (array, required): Array of competitor data points
- `currentCustomer` (number, optional): ID of current customer to highlight

**Data Format:**
```javascript
[
  {
    id: 117,
    domain: 'bethard.com',
    links: 56,
    quality: 80.1
  },
  // ... more competitors
]
```

**Usage:**
```jsx
import { CompetitiveScatterPlot } from './components/charts';

const competitiveData = [
  { id: 117, domain: 'bethard.com', links: 56, quality: 80.1 },
  { id: 118, domain: 'casinostugan.com', links: 42, quality: 75.3 },
  { id: 119, domain: 'mrgreen.se', links: 68, quality: 82.5 },
  { id: 120, domain: 'leovegas.com', links: 51, quality: 78.9 },
  { id: 121, domain: 'videoslots.com', links: 39, quality: 71.2 },
  { id: 122, domain: 'casumo.com', links: 73, quality: 85.4 }
];

<CompetitiveScatterPlot
  data={competitiveData}
  currentCustomer={117}
/>
```

**Features:**
- **Quadrant Analysis**: Automatic calculation of average lines
  - Top-right: High quality + High volume (🎯 Best position)
  - Top-left: High quality + Low volume
  - Bottom-right: Low quality + High volume
  - Bottom-left: Low quality + Low volume
- **Current Customer Highlighting**: Larger blue dot with stroke
- **Interactive Tooltips**: Shows domain, link count, and quality score
- **Reference Lines**: Dashed lines for averages

---

## 🎯 Import Methods

### Individual Imports
```jsx
import HealthGauge from './components/charts/HealthGauge';
import AnchorDistributionChart from './components/charts/AnchorDistributionChart';
```

### Batch Import (Recommended)
```jsx
import {
  HealthGauge,
  AnchorDistributionChart,
  TemporalChart,
  MonthlyDistributionChart,
  DomainDistributionChart,
  TLDDistributionChart,
  CompetitiveScatterPlot
} from './components/charts';
```

---

## 🎨 Design System

All charts follow LinkDB's color palette:

### Primary Colors
- **Blue**: `#3b82f6` - Primary action/default
- **Green**: `#10b981` - Success/positive
- **Yellow**: `#f59e0b` - Warning/caution
- **Red**: `#ef4444` - Error/negative
- **Purple**: `#8b5cf6` - Secondary/accent
- **Gray**: `#6b7280` - Neutral

### Tooltip Styling
All custom tooltips use:
- White background (`bg-white`)
- Border gray 200 (`border-gray-200`)
- Shadow large (`shadow-lg`)
- Rounded corners (`rounded`)
- Padding 12px (`p-3`)

---

## 📱 Responsive Design

All charts use `ResponsiveContainer` from Recharts:
- **Width**: 100% (adapts to parent container)
- **Height**: Fixed values (300px or 400px)
- Charts automatically resize on window resize

---

## 🧪 Testing

To test charts, create a test page with sample data:

```jsx
// TestChartsPage.jsx
import React from 'react';
import {
  HealthGauge,
  AnchorDistributionChart,
  TemporalChart,
  MonthlyDistributionChart,
  DomainDistributionChart,
  TLDDistributionChart,
  CompetitiveScatterPlot
} from './components/charts';

const TestChartsPage = () => {
  return (
    <div className="p-8 space-y-12">
      <section>
        <h2 className="text-2xl font-bold mb-4">Health Gauge</h2>
        <HealthGauge score={80.1} label="Overall Health" />
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-4">Anchor Distribution</h2>
        <AnchorDistributionChart
          data={[
            { name: 'exact', value: 25 },
            { name: 'partial', value: 35 },
            { name: 'branded', value: 25 },
            { name: 'generic', value: 15 }
          ]}
        />
      </section>

      {/* Add more chart sections... */}
    </div>
  );
};

export default TestChartsPage;
```

---

## 🚀 Performance Tips

1. **Memoize Data**: Use `React.useMemo` for data transformations
2. **Debounce Resize**: Charts handle resize automatically
3. **Lazy Loading**: Consider code-splitting for large dashboards
4. **Data Pagination**: Limit data points for scatter plots (50-100 max)

---

## 🐛 Troubleshooting

### Charts not rendering?
- Ensure parent container has defined dimensions
- Check that data format matches expected structure
- Verify Recharts is installed: `npm list recharts`

### Tooltips not showing?
- Check that custom tooltip receives correct props
- Ensure white background and proper z-index

### Colors not appearing?
- Verify Tailwind CSS is configured
- Check that color values are correct hex codes

---

## 📚 References

- [Recharts Documentation](https://recharts.org/)
- [Recharts GitHub](https://github.com/recharts/recharts)
- [React Documentation](https://react.dev/)

---

## ✅ Handoff to Track 4

**Status**: ✅ All chart components ready for integration

**What's Included**:
- ✅ 7 fully functional chart components
- ✅ Custom tooltips for all charts
- ✅ Responsive containers
- ✅ Proper color coding
- ✅ Interactive features
- ✅ TypeScript-ready (can add .d.ts files if needed)

**Next Steps for Track 4**:
1. Import charts into page components
2. Connect to backend API data
3. Add loading states
4. Implement error boundaries
5. Add data refresh functionality

**Example Integration**:
```jsx
// In your page component (Track 4)
import { HealthGauge, CompetitiveScatterPlot } from '../components/charts';

const DashboardPage = () => {
  const [healthScore, setHealthScore] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from backend
    fetch('/api/health-score')
      .then(res => res.json())
      .then(data => {
        setHealthScore(data.score);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Dashboard</h1>
      <HealthGauge score={healthScore} label="Link Health" />
    </div>
  );
};
```

---

**Built with ❤️ by Track 3 - Data Visualization Specialist**

*Ready for production use! 🚀*
