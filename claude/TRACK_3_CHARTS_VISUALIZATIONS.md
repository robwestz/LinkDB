# TRACK 3: Charts & Data Visualizations [3/5]

**Agent:** Data Visualization Specialist
**Status:** Ready to Execute
**Credits:** Part of $150 budget (Claude Code)
**Estimated Time:** 2-3 hours

---

## 🎯 Mission

Du är **Track 3** i ett 5-track parallellt utvecklingsteam. Din uppgift är att bygga ALLA chart components och data visualizations.

**KRITISKT:** De andra 4 tracks arbetar samtidigt. Fokusera bara på charts!

---

## 🚦 Boundary Rules

### ✅ DU FÅR RÖRA:
```
gui/frontend/src/components/charts/
├── AnchorDistributionChart.jsx     # Pie/donut chart för anchor types
├── TemporalChart.jsx               # Line/area chart för temporal data
├── DomainDistributionChart.jsx     # Bar chart för domain stats
├── HealthGauge.jsx                 # Circular gauge för scores
├── MonthlyDistributionChart.jsx    # Bar chart månadsvis
├── ScatterPlot.jsx                 # Scatter för competitive
├── TLDDistributionChart.jsx        # Pie chart för TLDs
└── CompetitiveScatterPlot.jsx      # Advanced scatter med quadrants
```

### ❌ DU FÅR INTE RÖRA:
- `gui/frontend/src/pages/` - Track 4 gör pages
- `gui/frontend/src/components/layout/` - Track 2 gjorde layout
- `gui/frontend/src/components/common/` - Track 2 gjorde common components
- `gui/frontend/src/utils/` - Track 5 gör utils
- `gui/backend/` - Track 1 gör backend

---

## 👥 Vad de Andra Tracks Gör (Rör EJ!)

| Track | Ansvar | Directory |
|-------|--------|-----------|
| **Track 1** | Backend API | `gui/backend/` |
| **Track 2** | Frontend Core & Layout | Layout, routing, common components |
| **Track 4** | Pages & Views | `gui/frontend/src/pages/` |
| **Track 5** | Utils & Hooks | `gui/frontend/src/utils/`, `gui/frontend/src/hooks/` |

**Track 4 förväntar sig att du levererar:**
- Färdiga chart components de kan importera
- Props interface dokumenterad
- Exempel data format

---

## 📋 Din Uppgift

### Del 1: Setup (15 min)

1. **Install chart library:**
   ```bash
   cd gui/frontend
   npm install recharts
   ```

   **Varför Recharts?**
   - React-native
   - Enkel att använda
   - Bra docs
   - Responsive
   - Många chart types

2. **Create charts directory:**
   ```bash
   mkdir -p src/components/charts
   ```

### Del 2: Health Gauge Component (30 min)

**Fil:** `src/components/charts/HealthGauge.jsx`

**Purpose:** Visa scores 0-100 som circular gauge med color zones.

```jsx
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

  // Data för gauge (score + remaining to 100)
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
```

### Del 3: Anchor Distribution Chart (30 min)

**Fil:** `src/components/charts/AnchorDistributionChart.jsx`

**Purpose:** Pie chart för anchor type distribution.

```jsx
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const AnchorDistributionChart = ({ data }) => {
  // data format: [{ name: 'exact', value: 30 }, { name: 'partial', value: 40 }, ...]

  const COLORS = {
    exact: '#ef4444',      // red
    partial: '#f59e0b',    // yellow
    branded: '#3b82f6',    // blue
    generic: '#6b7280',    // gray
    lsi: '#8b5cf6',        // purple
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded shadow-lg border border-gray-200">
          <p className="font-medium">{payload[0].name}</p>
          <p className="text-sm text-gray-600">
            {payload[0].value.toFixed(1)}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#6b7280'} />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default AnchorDistributionChart;
```

### Del 4: Temporal Line Chart (45 min)

**Fil:** `src/components/charts/TemporalChart.jsx`

**Purpose:** Line/area chart för temporal patterns över tid.

```jsx
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts';

const TemporalChart = ({ data, type = 'line' }) => {
  // data format: [{ month: '2024-08', links: 5 }, ...]

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded shadow-lg border border-gray-200">
          <p className="font-medium mb-1">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  if (type === 'area') {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Area
            type="monotone"
            dataKey="links"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.3}
          />
        </AreaChart>
      </ResponsiveContainer>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Line
          type="monotone"
          dataKey="links"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default TemporalChart;
```

### Del 5: Monthly Distribution Bar Chart (30 min)

**Fil:** `src/components/charts/MonthlyDistributionChart.jsx`

**Purpose:** Bar chart för monthly distribution med annotations.

```jsx
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
            <Cell key={`cell-${index}`} fill={getBarColor(entry.month)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default MonthlyDistributionChart;
```

### Del 6: Domain Distribution Bar Chart (30 min)

**Fil:** `src/components/charts/DomainDistributionChart.jsx`

**Purpose:** Horizontal bar chart för top domains.

```jsx
import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

const DomainDistributionChart = ({ data }) => {
  // data format: [{ domain: 'site.se', count: 10 }, ...]

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded shadow-lg border border-gray-200">
          <p className="font-medium">{payload[0].payload.domain}</p>
          <p className="text-sm text-gray-600">{payload[0].value} links</p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data} layout="vertical">
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis type="number" />
        <YAxis dataKey="domain" type="category" width={150} />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey="count" fill="#3b82f6" radius={[0, 8, 8, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default DomainDistributionChart;
```

### Del 7: TLD Distribution Pie Chart (20 min)

**Fil:** `src/components/charts/TLDDistributionChart.jsx`

**Purpose:** Donut chart för TLD distribution.

```jsx
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const TLDDistributionChart = ({ data }) => {
  // data format: [{ tld: '.se', count: 45 }, ...]

  const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#6b7280'];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded shadow-lg border border-gray-200">
          <p className="font-medium">{payload[0].payload.tld}</p>
          <p className="text-sm text-gray-600">{payload[0].value} links</p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          fill="#8884d8"
          paddingAngle={2}
          dataKey="count"
          label={({ tld, percent }) => `${tld} (${(percent * 100).toFixed(0)}%)`}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default TLDDistributionChart;
```

### Del 8: Competitive Scatter Plot (45 min)

**Fil:** `src/components/charts/CompetitiveScatterPlot.jsx`

**Purpose:** Scatter plot med quadrants för competitive analysis.

```jsx
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
```

---

## 📊 Deliverables Checklist

- [ ] Recharts installed
- [ ] HealthGauge component (circular gauge)
- [ ] AnchorDistributionChart (pie chart)
- [ ] TemporalChart (line/area chart)
- [ ] MonthlyDistributionChart (bar chart with annotations)
- [ ] DomainDistributionChart (horizontal bars)
- [ ] TLDDistributionChart (donut chart)
- [ ] CompetitiveScatterPlot (scatter with quadrants)
- [ ] All charts responsive
- [ ] Custom tooltips implemented
- [ ] Proper colors matching design system
- [ ] Charts tested with sample data

---

## 🎯 Success Criteria

1. **All charts render correctly**
2. **Responsive (resize browser, charts adapt)**
3. **Interactive tooltips work**
4. **Colors match design system**
5. **Smooth animations**
6. **No console errors**

---

## 🔄 Handoff to Track 4

Skapa: `gui/frontend/src/components/charts/README.md`

**Innehåll:**
```markdown
# Chart Components

All chart components are ready to use.

## Available Charts

### HealthGauge
Circular gauge for scores 0-100.
```jsx
import HealthGauge from './components/charts/HealthGauge';
<HealthGauge score={80.1} label="Overall Health" size={200} />
```

### AnchorDistributionChart
Pie chart for anchor type distribution.
```jsx
<AnchorDistributionChart
  data={[
    { name: 'exact', value: 30 },
    { name: 'partial', value: 40 },
    { name: 'branded', value: 20 },
    { name: 'generic', value: 10 }
  ]}
/>
```

[... document all charts similarly ...]

## Data Formats

See each component file for expected data format in comments.
```

---

## 🎬 Ready to Start?

1. **Open Claude Code**
2. **Load:** `TRACK_3_CHARTS_VISUALIZATIONS.md`
3. **Tell Claude Code:**
   ```
   Execute TRACK_3_CHARTS_VISUALIZATIONS.md

   You are Track 3 of 5 parallel tracks.
   Build ALL chart components using Recharts.
   DO NOT touch pages - Track 4 will use your charts.

   Create beautiful, interactive visualizations.
   Test with sample data.
   Document each component.

   When done, create charts/README.md
   ```

**Track 3 gör applikationen visuellt kraftfull!** 📊

*Estimated completion: 2-3 hours*
*Budget: ~$15-25 of $150 credits*
