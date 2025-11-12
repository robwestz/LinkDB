# LinkDB Advanced Analytics GUI - Complete Specification for Gemini

**IMPORTANT INSTRUCTIONS FOR GEMINI:**
- This is NOT an MVP. This is a **near-final beta version** GUI.
- You have NO token limitations. Use as many as needed to create something **exceptional**.
- Think "overkill and then double it" in terms of:
  - Visual polish
  - Feature completeness
  - User experience
  - Data visualization
  - Interactivity
  - Professional design
- DO NOT touch or modify ANY existing files
- Create ALL new GUI files in a NEW directory: `gui/` or `web_gui/`
- Use modern web technologies (suggest: React/Vue/Svelte OR Python Flask/FastAPI with Jinja2)
- Assume you're building for a professional SEO agency that will show this to clients

---

## 🎯 Project Overview

LinkDB is a sophisticated backlink analysis and strategic planning system for SEO agencies managing 210+ customers with 4,700+ historical links.

**Your mission:** Create a stunning, professional-grade web GUI that showcases ALL the analytical power we've built.

---

## 📂 Project Structure

### Current Backend (DO NOT MODIFY)
```
linkdb/
├── data/
│   └── output/
│       ├── linkops_history.db          # Main database
│       └── customers/                   # 210 customer DBs
│           └── [domain]/
│               └── customer.db
├── app/
│   ├── analyzers/
│   │   ├── link_history_analyzer.py     # Strategy & patterns
│   │   ├── anchor_quality_analyzer.py   # Anchor quality & over-optimization
│   │   ├── temporal_pattern_analyzer.py # Velocity, gaps, spikes
│   │   ├── domain_quality_analyzer.py   # Domain diversity, PBN detection
│   │   └── competitive_comparison.py    # Benchmarking
│   └── history_repo.py                  # Database interface
└── comprehensive_analytics.py           # Runs all analyzers
```

### New GUI Structure (TO BE CREATED BY YOU)
```
linkdb/
├── gui/                                 # NEW DIRECTORY
│   ├── app.py                          # Main Flask/FastAPI app (or index.html for React)
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   ├── dashboard.css
│   │   │   ├── charts.css
│   │   │   └── components.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── charts.js               # Chart.js, D3.js, or Recharts
│   │   │   ├── filters.js
│   │   │   └── api.js
│   │   └── img/
│   │       └── logos/
│   ├── templates/                       # If using Flask/Jinja
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── customer_analysis.html
│   │   ├── competitive_benchmarking.html
│   │   ├── link_explorer.html
│   │   └── components/
│   │       ├── metrics_card.html
│   │       ├── chart_card.html
│   │       └── table_card.html
│   ├── components/                      # If using React/Vue
│   │   ├── Dashboard.jsx
│   │   ├── CustomerAnalysis.jsx
│   │   ├── CompetitiveBenchmark.jsx
│   │   ├── LinkExplorer.jsx
│   │   └── charts/
│   │       ├── AnchorDistribution.jsx
│   │       ├── TemporalChart.jsx
│   │       ├── DomainMap.jsx
│   │       └── HealthGauge.jsx
│   ├── api/
│   │   └── routes.py                   # API endpoints
│   └── requirements.txt                # GUI dependencies
└── README_GUI.md                        # How to run the GUI
```

---

## 🎨 Design System

### Color Palette (Professional SEO Agency Theme)
```css
/* Primary Colors */
--primary-blue: #2563eb;           /* Trust, professionalism */
--primary-dark: #1e40af;
--primary-light: #60a5fa;

/* Success/Warning/Danger */
--success-green: #10b981;
--warning-yellow: #f59e0b;
--danger-red: #ef4444;

/* Neutrals */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-700: #374151;
--gray-900: #111827;

/* Chart Colors */
--chart-1: #3b82f6;
--chart-2: #8b5cf6;
--chart-3: #ec4899;
--chart-4: #f59e0b;
--chart-5: #10b981;
```

### Typography
```css
/* Font Family */
font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Spacing & Layout
```css
/* Spacing Scale */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */

/* Border Radius */
--radius-sm: 0.25rem;
--radius-md: 0.5rem;
--radius-lg: 0.75rem;
--radius-xl: 1rem;

/* Shadows */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
```

---

## 📱 Main Views & Features

### 1. **Dashboard (Home Page)**
**URL:** `/` or `/dashboard`

**Purpose:** Executive overview with key metrics across all customers or selected customer.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  LinkDB Analytics                          [User Menu]   │
├──────────┬──────────────────────────────────────────────┤
│          │  Dashboard > Overview                         │
│  SIDEBAR │                                               │
│          │  ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│ - Dashb. │  │ 210     │ │ 4,736   │ │ 80.1    │        │
│ - Custom │  │Customer │ │ Links   │ │ Avg Scr │        │
│ - Compet │  └─────────┘ └─────────┘ └─────────┘        │
│ - Links  │                                               │
│ - Settin │  ┌────────────────────────────────┐          │
│          │  │  Customer Health Distribution  │          │
│          │  │  [BAR CHART: Health tiers]     │          │
│          │  └────────────────────────────────┘          │
│          │                                               │
│          │  ┌────────────────────────────────┐          │
│          │  │  Recent Activity Timeline      │          │
│          │  │  [TIMELINE CHART]              │          │
│          │  └────────────────────────────────┘          │
│          │                                               │
│          │  ┌──────────┬──────────────────────┐         │
│          │  │ Top 10   │  Alerts & Warnings   │         │
│          │  │ Perf.    │  [LIST]              │         │
│          │  └──────────┴──────────────────────┘         │
└──────────┴──────────────────────────────────────────────┘
```

**KPI Cards (Top Row):**
1. **Total Customers**
   - Number: 210
   - Trend: +5 this month
   - Icon: Users icon

2. **Total Links**
   - Number: 4,736
   - Trend: +127 this month
   - Icon: Link icon

3. **Average Health Score**
   - Number: 80.1 / 100
   - Visual: Mini gauge/progress ring
   - Icon: Heart pulse icon

4. **Quality Grade**
   - Grade: A-
   - Distribution: 45% A, 30% B, 15% C, 10% D
   - Icon: Star icon

**Charts:**

1. **Customer Health Distribution** (Bar Chart)
   - X-axis: Health score ranges (0-20, 21-40, 41-60, 61-80, 81-100)
   - Y-axis: Number of customers
   - Color: Gradient from red → yellow → green
   - Interactive: Click to filter customers

2. **Activity Timeline** (Line/Area Chart)
   - X-axis: Last 12 months
   - Y-axis: Number of links built
   - Multiple lines:
     - Total links (primary)
     - High quality links (green)
     - Risky links (red)
   - Interactive: Hover for details, click to drill down

3. **Top 10 Performers** (Table + Sparklines)
   ```
   | Rank | Customer        | Links | Health | Trend    |
   |------|----------------|-------|--------|----------|
   | 1    | bethard.com    | 56    | 80.1   | ↗ [mini] |
   | 2    | flaxcasino.se  | 73    | 85.2   | → [mini] |
   ...
   ```

4. **Alerts & Warnings** (Card List)
   ```
   ⚠️ bethard.com: High over-optimization risk (51.8% exact match)
   ⚠️ casino123.se: PBN risk detected (cross-linking score: 75)
   💡 acnespecialisten.se: Low velocity - opportunity to increase
   ✅ flaxcasino.se: Excellent health, maintain current strategy
   ```

**Filters (Top Bar):**
- Customer search/select (dropdown with autocomplete)
- Date range picker
- Health score range slider
- Industry filter

---

### 2. **Customer Analysis (Deep Dive)**
**URL:** `/customer/<id>` or `/customer?domain=bethard.com`

**Purpose:** Complete analysis for a single customer using ALL analyzers.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  bethard.com                                   [Export]  │
├──────────┬──────────────────────────────────────────────┤
│          │  Customer Analysis > bethard.com              │
│  SIDEBAR │                                               │
│          │  ┌─────────────────────────────────────────┐ │
│          │  │  EXECUTIVE SUMMARY                      │ │
│          │  │  Overall Score: 80.1 / 100              │ │
│          │  │  Assessment: EXCELLENT                  │ │
│          │  │  [Circular gauge visualization]         │ │
│          │  └─────────────────────────────────────────┘ │
│          │                                               │
│          │  ┌───┬───┬───┬───┬───┐  [Tab Navigation]     │
│          │  │ 1 │ 2 │ 3 │ 4 │ 5 │                       │
│          │  └───┴───┴───┴───┴───┘                       │
│          │                                               │
│          │  [Tab Content Area - see below]              │
│          │                                               │
└──────────┴──────────────────────────────────────────────┘
```

**Tab 1: Overview & Strategy**
- **Link Portfolio Card:**
  - Total links: 56
  - Unique domains: 51
  - Target URLs: 11
  - Date range: Aug 2024 - Oct 2025
  - Primary strategy: focused_single_page

- **Key Metrics Grid:**
  ```
  ┌──────────────┬──────────────┬──────────────┐
  │ Anchor Q.    │ Temporal H.  │ Domain Q.    │
  │ 59.9 / 100   │ 85.2 / 100   │ 95.0 / 100   │
  │ [gauge]      │ [gauge]      │ [gauge]      │
  └──────────────┴──────────────┴──────────────┘
  ```

- **Top 3 Priority Recommendations:**
  ```
  1. [Anchor] ⚠️ 51.8% exact match anchors - diversify immediately
  2. [Anchor] ⚠️ 69.6% commercial keywords - reduce aggressiveness
  3. [Strategy] ✅ Excellent domain diversity - maintain this approach
  ```

**Tab 2: Anchor Text Analysis**
- **Anchor Quality Gauge:**
  - Large circular gauge showing 59.9/100
  - Color-coded zones (red/yellow/green)
  - Over-optimization risk indicator: HIGH (red banner)

- **Diversity Metrics:**
  ```
  Shannon Entropy:     5.39
  Diversity Score:     92.8/100  [progress bar]
  Gini Coefficient:    0.161     [explanation tooltip]
  Top 10 Concentration: 35.7%    [pie chart]
  ```

- **Anchor Distribution Pie Chart:**
  - Exact match: 51.8% (red)
  - Branded: 3.6% (blue)
  - Commercial: 69.6% (orange overlay indicator)
  - Interactive: Click slices to see anchor list

- **Top Anchors Table:**
  ```
  | Rank | Anchor Text         | Count | % | Type    | Risk  |
  |------|---------------------|-------|---|---------|-------|
  | 1    | Betting             | 4     | 7%| Exact   | ⚠️ Med|
  | 2    | Bethard             | 3     | 5%| Brand   | ✅ Low|
  | 3    | bethard             | 3     | 5%| Brand   | ✅ Low|
  ...
  ```

- **Warnings & Recommendations:**
  - Collapsible alert boxes with icons
  - Color-coded by severity
  - Action buttons ("Fix this", "Learn more")

**Tab 3: Temporal Patterns**
- **Health Score Gauge:** 85.2/100

- **Velocity Metrics Cards:**
  ```
  ┌────────────┬────────────┬────────────┐
  │ Per Day    │ Per Week   │ Per Month  │
  │ 0.14       │ 1.0        │ 4.1        │
  │ [icon]     │ [icon]     │ [icon]     │
  └────────────┴────────────┴────────────┘
  ```

- **Monthly Distribution Chart:**
  - Bar chart showing links per month
  - X-axis: 2024-08 to 2025-10
  - Y-axis: Number of links
  - Hover: Show exact count + anchor type breakdown
  - Annotations: Mark best month, worst month, spikes

- **Consistency Visualizer:**
  - Line chart of monthly variance
  - Highlighted gaps (>30 days)
  - Trend line (increasing/stable/decreasing)
  - Coefficient of Variation: 0.39 (Good)

- **Spike Detection:**
  - ✅ No unnatural spikes detected (green checkmark)
  - OR: ⚠️ Spikes detected in: [list months]

**Tab 4: Domain Quality**
- **Quality Score Gauge:** 95.0/100

- **Domain Distribution:**
  ```
  Total Domains:       56
  Unique Domains:      51
  Diversity Score:     91.1/100
  PBN Risk Score:      0/100  (✅ Excellent)
  ```

- **TLD Distribution Pie Chart:**
  - .se: 80.4% (45 links)
  - .nu: 8.9% (5 links)
  - .net, .com, .io, .tv: smaller slices
  - Interactive: Click to filter domain list

- **Geographic Diversity Map:**
  - Simple world map (or Europe map) with pins
  - Sweden: 45 links (largest)
  - Other countries: smaller markers
  - Tooltip on hover: Country name + count

- **Top Domains Table:**
  ```
  | Rank | Domain              | Links | % | Type       | Quality |
  |------|---------------------|-------|---|------------|---------|
  | 1    | totallyorebro.se    | 3     | 5%| News       | ✅ High |
  | 2    | executiveeffect.se  | 2     | 4%| Business   | ✅ High |
  ...
  ```

- **Risk Assessment:**
  - Cross-linking score: 0/100 (✅ Safe)
  - Power domains: 0 (may need more authority)
  - Single-link domains: 47 (good diversity)

**Tab 5: Competitive Benchmarking**
- **Percentile Rankings:**
  ```
  ┌─────────────────────────┐
  │  Volume: 75th percentile│
  │  [Bar showing position] │
  │  Top 25% of industry    │
  └─────────────────────────┘

  ┌─────────────────────────┐
  │  Quality: 82nd percentile│
  │  [Bar showing position] │
  │  Top 20% of industry    │
  └─────────────────────────┘
  ```

- **Industry Comparison:**
  ```
  Your Links:        56
  Industry Average:  37.7
  Industry Median:   28
  Difference:        +18.3 above average
  ```

- **Performance vs Competitors:**
  - Scatter plot:
    - X-axis: Number of links
    - Y-axis: Quality score
    - Your customer: Highlighted in blue
    - Others: Gray dots
    - Quadrants labeled: "Low volume, low quality" etc.

- **Gap Analysis:**
  ```
  Strengths:
  ✅ Domain diversity (Top 10%)
  ✅ Temporal consistency (Top 20%)

  Opportunities:
  ⚠️ Anchor quality (Bottom 40%)
  💡 Link volume (Can increase by 15% to match top 10%)
  ```

**Export Options (Top Right):**
- Export as PDF report
- Export data as CSV/Excel
- Share link (generate shareable URL)
- Schedule automated report

---

### 3. **Competitive Benchmarking Dashboard**
**URL:** `/competitive` or `/benchmarking`

**Purpose:** Industry-wide view comparing all customers.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Competitive Benchmarking                    [Filters]   │
├──────────┬──────────────────────────────────────────────┤
│          │  Industry Overview                            │
│  SIDEBAR │                                               │
│          │  ┌───────────────────────────────────────┐   │
│          │  │  Total Customers: 210                 │   │
│          │  │  Total Links: 4,736                   │   │
│          │  │  Avg Links/Customer: 22.6             │   │
│          │  │  Median: 15                           │   │
│          │  └───────────────────────────────────────┘   │
│          │                                               │
│          │  ┌───────────────────────────────────────┐   │
│          │  │  Volume Distribution                  │   │
│          │  │  [Histogram chart]                    │   │
│          │  └───────────────────────────────────────┘   │
│          │                                               │
│          │  ┌───────────────────────────────────────┐   │
│          │  │  Quality Tiers                        │   │
│          │  │  [Donut chart]                        │   │
│          │  └───────────────────────────────────────┘   │
│          │                                               │
│          │  ┌────────────────────────────────────┬──┐   │
│          │  │ Top 10 by Volume   │ Top 10 Quality│   │
│          │  │ [Leaderboard]      │ [Leaderboard] │   │
│          │  └────────────────────────────────────┴──┘   │
└──────────┴──────────────────────────────────────────────┘
```

**Features:**

1. **Volume Distribution Histogram:**
   - X-axis: Link count ranges (0-10, 11-25, 26-50, 51-100, 100+)
   - Y-axis: Number of customers
   - Color gradient: Light blue to dark blue
   - Hover: Show customer count + percentage

2. **Quality Tiers Donut Chart:**
   - Segments:
     - Excellent (80-100): 30% - Green
     - Good (60-79): 35% - Light green
     - Fair (40-59): 25% - Yellow
     - Poor (0-39): 10% - Red
   - Center: "210 Total"
   - Interactive: Click to filter table

3. **Leaderboards (Side-by-Side):**
   ```
   Top 10 by Volume              Top 10 by Quality
   ┌─────────────────────┐      ┌─────────────────────┐
   │ 1. domain.se   123  │      │ 1. site.com   98.5  │
   │ 2. site.com    98   │      │ 2. best.se    97.2  │
   │ 3. best.se     87   │      │ 3. top.no     95.1  │
   │ ...                 │      │ ...                 │
   └─────────────────────┘      └─────────────────────┘
   ```

4. **Customer Comparison Table:**
   ```
   | Customer        | Links | Domains | Anchor Q | Temporal | Domain Q | Overall | Trend |
   |-----------------|-------|---------|----------|----------|----------|---------|-------|
   | bethard.com     | 56    | 51      | 59.9     | 85.2     | 95.0     | 80.1    | ↗     |
   | flaxcasino.se   | 73    | 68      | 72.3     | 88.5     | 92.1     | 84.3    | ↗     |
   ...
   ```
   - Sortable columns
   - Click row to navigate to customer detail
   - Color-coded cells (green = above avg, red = below avg)
   - Search bar above table

5. **Scatter Plot Matrix:**
   - Multiple scatter plots comparing:
     - Links vs Quality
     - Diversity vs Health
     - Velocity vs Consistency
   - Interactive: Click point to highlight customer

**Filters:**
- Link volume range (slider)
- Quality score range (slider)
- Industry/category (dropdown)
- Date range (picker)
- TLD filter (.se, .com, etc)

---

### 4. **Link Explorer**
**URL:** `/links` or `/explorer`

**Purpose:** Browse, search, and filter all links in the database.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Link Explorer                              [Export CSV] │
├──────────┬──────────────────────────────────────────────┤
│          │  ┌─────────────────────────────────────┐     │
│  FILTERS │  │  Search: [________________] 🔍      │     │
│          │  └─────────────────────────────────────┘     │
│ Customer │                                               │
│ [Select] │  Showing 1-50 of 4,736 links                 │
│          │                                               │
│ Date     │  ┌──────────────────────────────────────┐    │
│ [Range]  │  │ | Customer | Pub Domain | Target... │    │
│          │  │ ├──────────┼────────────┼──────────┤│    │
│ Anchor   │  │ │bethard..│ site.se    │ https... ││    │
│ Type     │  │ │[More details...]                  │    │
│ [Multi]  │  │ ├───────────────────────────────────┤│    │
│          │  │ │ ...                               ││    │
│ Domain   │  │ └──────────────────────────────────────┘    │
│ [Input]  │  │                                               │
│          │  │  [Pagination: < 1 2 3 ... 95 >]            │
│ Target   │  │                                               │
│ URL      │  └──────────────────────────────────────────────┘
│ [Input]  │
│          │
│ Quality  │
│ [Slider] │
└──────────┴──────────────────────────────────────────────┘
```

**Table Columns:**
- Customer (with logo if available)
- Publishing Domain
- Publishing URL (truncated, tooltip on hover)
- Target Domain
- Target URL (truncated)
- Anchor Text (with type badge)
- Link Type (badge: guest_post, editorial, etc)
- Language (flag icon)
- Published Date
- Quality Indicators (icons/badges)
  - ✅ Safe
  - ⚠️ Medium risk
  - 🚨 High risk

**Expandable Rows:**
- Click row to expand and show:
  - Full URLs
  - Context excerpt (if available)
  - Topic tags
  - All metadata
  - Mini chart of customer's anchor distribution
  - Action buttons:
    - "View Customer Analysis"
    - "Flag as risky"
    - "Add note"

**Bulk Actions:**
- Select multiple rows (checkboxes)
- Actions dropdown:
  - Export selected
  - Tag selected
  - Delete selected (with confirmation)
  - Assign to campaign

**Advanced Filters Panel:**
- Collapsible sidebar with:
  - Customer multi-select
  - Date range picker (with presets: This month, Last 3 months, etc)
  - Anchor type checkboxes (exact, partial, branded, generic, LSI)
  - Domain input (search by pub or target domain)
  - Target URL input
  - Quality slider (0-100)
  - Risk level (safe, medium, high)
  - Language multi-select
  - Link type multi-select
  - Has context excerpt (yes/no toggle)
  - Has topic tags (yes/no toggle)

**Real-time Count:**
- As filters applied, show: "Showing X of Y links"

---

### 5. **Settings & Configuration**
**URL:** `/settings`

**Features:**
- Database settings (path, backup)
- Analysis thresholds configuration:
  - Over-optimization threshold (default: 40% exact match)
  - Spike detection sensitivity
  - PBN risk thresholds
- Export templates
- User preferences:
  - Default customer view
  - Date format
  - Chart preferences
- API keys (for future SERP scraping)
- Notification settings

---

## 📊 Advanced Visualizations

### Chart Types to Implement

1. **Circular Gauges** (for scores 0-100)
   - Use libraries: Chart.js with chartjs-gauge, or Recharts RadialBarChart
   - Color zones:
     - 0-40: Red
     - 41-60: Orange
     - 61-80: Yellow
     - 81-100: Green
   - Animate on load

2. **Multi-line Time Series**
   - Library: Chart.js, Recharts LineChart, or D3.js
   - Features:
     - Multiple datasets (total, quality, risky)
     - Zoom & pan
     - Crosshair on hover
     - Legend toggle (click to show/hide line)
     - Annotations for key events

3. **Stacked Bar Charts**
   - For anchor type distribution over time
   - X-axis: Months
   - Y-axis: Number of anchors
   - Stack colors: exact, partial, branded, generic, LSI

4. **Heatmap Calendar**
   - Github-style contribution graph
   - Shows link building activity per day
   - Color intensity = number of links
   - Tooltip: Date, count, quality average

5. **Treemap**
   - For domain distribution
   - Rectangle size = number of links from that domain
   - Color = quality score
   - Click to drill down

6. **Sankey Diagram**
   - Flow from Publishing Domains → Target Domains
   - Width = number of links
   - Color by quality
   - Interactive: Hover to highlight paths

7. **Network Graph**
   - Nodes: Domains
   - Edges: Links
   - Size: Link count
   - Color: Quality
   - Interactive: Drag nodes, zoom, filter

8. **Radar Chart**
   - Compare customer against industry on multiple dimensions:
     - Volume
     - Quality
     - Diversity
     - Consistency
     - Domain strength
   - Overlay: Customer (filled blue) vs Industry avg (outline gray)

---

## 🎨 UI Components Library

Create reusable components:

### 1. **MetricCard**
```jsx
<MetricCard
  title="Total Links"
  value="56"
  change="+12"
  changePercent="27%"
  trend="up"
  icon="link"
  color="blue"
/>
```
Visual:
```
┌────────────────────────┐
│ 🔗 Total Links         │
│                        │
│     56                 │
│     +12 (27%) ↗        │
└────────────────────────┘
```

### 2. **ScoreGauge**
```jsx
<ScoreGauge
  score={80.1}
  label="Overall Health"
  max={100}
  threshold={{
    poor: 40,
    fair: 60,
    good: 80
  }}
/>
```

### 3. **AlertBox**
```jsx
<AlertBox
  type="warning"
  title="High Over-Optimization Risk"
  message="51.8% exact match anchors detected"
  action={{
    label: "View Details",
    onClick: () => {}
  }}
/>
```
Visual:
```
┌────────────────────────────────────────┐
│ ⚠️ High Over-Optimization Risk         │
│                                        │
│ 51.8% exact match anchors detected    │
│                                        │
│ [View Details]                         │
└────────────────────────────────────────┘
```

### 4. **DataTable**
```jsx
<DataTable
  columns={[...]}
  data={[...]}
  searchable={true}
  sortable={true}
  pagination={true}
  pageSize={50}
  exportable={true}
  expandable={true}
  selectable={true}
/>
```
Features:
- Column sorting (click header)
- Search bar (filters all columns)
- Pagination controls
- Export to CSV/Excel
- Expandable rows (click to expand)
- Row selection (checkboxes)
- Responsive (collapses on mobile)

### 5. **FilterPanel**
```jsx
<FilterPanel
  filters={[
    { type: 'select', label: 'Customer', options: [...] },
    { type: 'daterange', label: 'Date Range' },
    { type: 'slider', label: 'Quality', min: 0, max: 100 },
    { type: 'multiselect', label: 'Anchor Types', options: [...] }
  ]}
  onFilterChange={(filters) => {}}
  onReset={() => {}}
/>
```

### 6. **ChartCard**
```jsx
<ChartCard
  title="Monthly Distribution"
  subtitle="Last 14 months"
  chart={<BarChart data={...} />}
  actions={[
    { label: 'Export PNG', onClick: () => {} },
    { label: 'View Data', onClick: () => {} }
  ]}
/>
```

---

## 🔌 API Endpoints (Backend)

Create a RESTful API for the GUI:

```python
# GET /api/customers
# Returns: List of all customers with basic stats

# GET /api/customers/<id>
# Returns: Full customer details

# GET /api/customers/<id>/analysis
# Returns: Complete analysis (all analyzers)
{
  "customer_id": 117,
  "canonical_root": "bethard.com",
  "link_history": { ... },
  "anchor_quality": { ... },
  "temporal_patterns": { ... },
  "domain_quality": { ... },
  "competitive_position": { ... }
}

# GET /api/customers/<id>/links
# Returns: All links for customer (paginated)

# GET /api/links
# Returns: All links (filterable, paginated)
# Query params: ?customer_id=X&anchor_type=exact&date_from=...

# GET /api/competitive/overview
# Returns: Industry benchmarks and top performers

# GET /api/competitive/compare?customer_id=X
# Returns: Customer vs industry comparison

# GET /api/dashboard/metrics
# Returns: Dashboard KPIs (total customers, links, avg scores)

# GET /api/export/customer/<id>
# Returns: PDF report or CSV data

# POST /api/analyze/customer/<id>
# Triggers: Re-run all analyzers (if data updated)
```

**Response Format:**
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2025-11-12T10:30:00Z",
    "execution_time_ms": 45,
    "cached": false
  },
  "errors": []
}
```

---

## 🚀 Technical Implementation Guide

### Recommended Tech Stack

**Option 1: Python Backend (Flask/FastAPI) + Vanilla JS/jQuery**
- **Backend:** Flask or FastAPI
- **Database:** SQLite (existing)
- **Templating:** Jinja2
- **Frontend:** Vanilla JavaScript or jQuery
- **Charts:** Chart.js
- **Styling:** Tailwind CSS or Bootstrap

**Pros:**
- Seamless integration with existing Python code
- No build process needed
- Quick to deploy
- Good for data-heavy apps

**Cons:**
- More server-side rendering
- Less snappy interactions

**Option 2: React/Next.js SPA + Python API**
- **Backend:** FastAPI (API only)
- **Frontend:** React with Next.js
- **Charts:** Recharts or Nivo
- **Styling:** Tailwind CSS
- **State:** React Query + Zustand

**Pros:**
- Modern, snappy UI
- Better user experience
- Component reusability
- Great for complex interactions

**Cons:**
- More complex setup
- Build process required
- Steeper learning curve

**Recommendation for this project:** **Option 2 (React + FastAPI)** if you want a modern, professional feel. **Option 1 (Flask + Jinja)** if you want faster development.

---

### Folder Structure (React Example)

```
gui/
├── backend/
│   ├── app.py                          # FastAPI main app
│   ├── routes/
│   │   ├── customers.py                # Customer endpoints
│   │   ├── links.py                    # Link endpoints
│   │   ├── competitive.py              # Benchmarking endpoints
│   │   └── dashboard.py                # Dashboard endpoints
│   ├── services/
│   │   ├── analyzer_service.py         # Calls analyzer modules
│   │   ├── database_service.py         # DB queries
│   │   └── export_service.py           # PDF/CSV generation
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── MetricCard.jsx
│   │   │   │   ├── ScoreGauge.jsx
│   │   │   │   ├── AlertBox.jsx
│   │   │   │   ├── DataTable.jsx
│   │   │   │   └── ChartCard.jsx
│   │   │   ├── charts/
│   │   │   │   ├── AnchorDistribution.jsx
│   │   │   │   ├── TemporalChart.jsx
│   │   │   │   ├── DomainMap.jsx
│   │   │   │   └── HealthGauge.jsx
│   │   │   └── layout/
│   │   │       ├── Sidebar.jsx
│   │   │       ├── Header.jsx
│   │   │       └── Layout.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── CustomerAnalysis.jsx
│   │   │   ├── CompetitiveBenchmarking.jsx
│   │   │   ├── LinkExplorer.jsx
│   │   │   └── Settings.jsx
│   │   ├── hooks/
│   │   │   ├── useCustomers.js         # React Query hook
│   │   │   ├── useLinks.js
│   │   │   └── useAnalysis.js
│   │   ├── utils/
│   │   │   ├── api.js                  # API client
│   │   │   ├── formatters.js           # Date/number formatting
│   │   │   └── colors.js               # Theme colors
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
│
└── README_GUI.md
```

---

## 🎨 Example Code Snippets

### FastAPI Backend (app.py)
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer
from app.analyzers.anchor_quality_analyzer import AnchorQualityAnalyzer
from app.analyzers.temporal_pattern_analyzer import TemporalPatternAnalyzer
from app.analyzers.domain_quality_analyzer import DomainQualityAnalyzer
from app.analyzers.competitive_comparison import CompetitiveComparison

app = FastAPI(title="LinkDB Analytics API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = str(Path(__file__).parent.parent / "data" / "output" / "linkops_history.db")

@app.get("/api/customers/{customer_id}/analysis")
def get_customer_analysis(customer_id: int):
    """Get complete analysis for a customer."""
    try:
        history_analyzer = LinkHistoryAnalyzer(DB_PATH)
        anchor_analyzer = AnchorQualityAnalyzer(DB_PATH)
        temporal_analyzer = TemporalPatternAnalyzer(DB_PATH)
        domain_analyzer = DomainQualityAnalyzer(DB_PATH)

        history = history_analyzer.analyze_customer(customer_id)
        anchor = anchor_analyzer.analyze_customer(customer_id)
        temporal = temporal_analyzer.analyze_customer(customer_id)
        domain = domain_analyzer.analyze_customer(customer_id)

        if not history:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Calculate overall score
        scores = []
        if anchor:
            scores.append(anchor.quality_score)
        if temporal:
            scores.append(temporal.health_score)
        if domain:
            scores.append(domain.quality_score)

        overall_score = sum(scores) / len(scores) if scores else 0

        return {
            "success": True,
            "data": {
                "customer_id": customer_id,
                "canonical_root": history.canonical_root,
                "brand": history.brand,
                "overall_score": round(overall_score, 1),
                "link_history": {
                    "total_links": history.total_links,
                    "unique_pub_domains": history.unique_pub_domains,
                    "unique_target_urls": history.unique_target_urls,
                    "links_per_month": round(history.links_per_month, 1),
                    "primary_strategy": history.primary_strategy,
                    "recommendations": history.recommendations,
                    "most_common_anchors": history.most_common_anchors,
                    "most_linked_urls": history.most_linked_urls
                },
                "anchor_quality": {
                    "quality_score": round(anchor.quality_score, 1),
                    "diversity_score": round(anchor.diversity_score, 1),
                    "over_optimization_risk": anchor.over_optimization_risk,
                    "shannon_entropy": round(anchor.shannon_entropy, 2),
                    "exact_match_ratio": round(anchor.exact_match_ratio * 100, 1),
                    "branded_ratio": round(anchor.branded_ratio * 100, 1),
                    "commercial_keywords_ratio": round(anchor.commercial_keywords_ratio * 100, 1),
                    "warnings": anchor.warnings,
                    "top_anchors": anchor.top_anchors
                } if anchor else None,
                "temporal_patterns": {
                    "health_score": round(temporal.health_score, 1),
                    "links_per_month": round(temporal.links_per_month, 1),
                    "velocity_trend": temporal.velocity_trend,
                    "consistency_score": round(temporal.consistency_score, 1),
                    "monthly_distribution": temporal.monthly_distribution,
                    "has_unnatural_spikes": temporal.has_unnatural_spikes,
                    "warnings": temporal.warnings,
                    "insights": temporal.insights
                } if temporal else None,
                "domain_quality": {
                    "quality_score": round(domain.quality_score, 1),
                    "unique_domains": domain.unique_domains,
                    "diversity_score": round(domain.domain_diversity_score, 1),
                    "cross_linking_score": round(domain.cross_linking_score, 1),
                    "top_tlds": domain.top_tlds,
                    "geographic_diversity": domain.geographic_diversity,
                    "warnings": domain.warnings,
                    "top_domains": domain.top_domains
                } if domain else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### React Component Example (MetricCard.jsx)
```jsx
import React from 'react';

const MetricCard = ({ title, value, change, changePercent, trend, icon, color = 'blue' }) => {
  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-600'
  };

  const bgColors = {
    blue: 'bg-blue-50',
    green: 'bg-green-50',
    red: 'bg-red-50',
    yellow: 'bg-yellow-50'
  };

  const iconColors = {
    blue: 'text-blue-600',
    green: 'text-green-600',
    red: 'text-red-600',
    yellow: 'text-yellow-600'
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-gray-600">{title}</h3>
        <div className={`p-3 rounded-full ${bgColors[color]}`}>
          <span className={`text-xl ${iconColors[color]}`}>{icon}</span>
        </div>
      </div>
      <div className="flex items-end justify-between">
        <div>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {change && (
            <p className={`text-sm mt-1 ${trendColors[trend]}`}>
              {trend === 'up' ? '↗' : trend === 'down' ? '↘' : '→'} {change} ({changePercent})
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default MetricCard;
```

---

## 🎯 Success Criteria

Your GUI should achieve:

### Visual Excellence
- ✅ Professional, modern design
- ✅ Consistent color scheme throughout
- ✅ Smooth animations and transitions
- ✅ Responsive layout (desktop + tablet, mobile optional)
- ✅ High contrast, accessible (WCAG AA)

### Functionality
- ✅ All 4 main analyzers fully integrated
- ✅ Real-time data from database (no mock data)
- ✅ Interactive charts (hover, click, zoom where appropriate)
- ✅ Filtering and search working
- ✅ Export functionality (at least CSV, bonus: PDF)
- ✅ Fast performance (<2s page load, <500ms interactions)

### User Experience
- ✅ Intuitive navigation
- ✅ Clear visual hierarchy
- ✅ Helpful tooltips and explanations
- ✅ Error handling with friendly messages
- ✅ Loading states (spinners, skeletons)
- ✅ Empty states (when no data)

### Code Quality
- ✅ Clean, organized code structure
- ✅ Reusable components
- ✅ Comments where necessary
- ✅ No console errors
- ✅ Proper error boundaries (React) or error pages (Flask)

---

## 📦 Deliverables

When you're done, provide:

1. **Complete GUI code** in `gui/` or `web_gui/` directory
2. **README_GUI.md** with:
   - How to install dependencies
   - How to run the backend (if separate)
   - How to run the frontend
   - How to access the GUI (which URL)
   - Any configuration needed
3. **Screenshots** in `gui/screenshots/` showing:
   - Dashboard
   - Customer analysis (all tabs)
   - Competitive benchmarking
   - Link explorer
4. **requirements.txt** or **package.json** (or both)

---

## 💎 Bonus Features (If You Have Time)

### Level 1 Bonuses
- Dark mode toggle
- User authentication (simple login)
- Favorite customers (bookmark feature)
- Customer notes (add comments to customers)
- Link tagging system

### Level 2 Bonuses
- Real-time updates (WebSocket for new links)
- Advanced filters saved as "views"
- Custom dashboard (drag & drop widgets)
- Comparison mode (compare 2 customers side-by-side)
- Historical snapshots (time travel to see customer at past date)

### Level 3 Bonuses
- AI-generated insights (LLM analysis of customer)
- Predictive analytics (forecast future scores)
- Anomaly detection alerts
- Automated reporting (schedule PDF reports via email)
- Multi-language support (Swedish + English)

---

## 🚨 Critical Reminders

1. **DO NOT modify any existing files** outside of `gui/` directory
2. **DO NOT change database schema** (read-only access)
3. **TEST with real data** from `linkops_history.db`
4. **Handle missing data gracefully** (some customers may have incomplete data)
5. **Optimize for performance** (lazy load charts, paginate tables)
6. **Make it beautiful** - this will be shown to clients!

---

## 🎬 Getting Started Checklist

- [ ] Read this entire specification (yes, all of it!)
- [ ] Decide on tech stack (Flask+Jinja OR React+FastAPI)
- [ ] Set up project structure in `gui/` directory
- [ ] Create API endpoints (start with `/api/customers/<id>/analysis`)
- [ ] Test API with Postman or browser
- [ ] Create basic layout (sidebar + header + content area)
- [ ] Implement Dashboard page with KPI cards
- [ ] Implement Customer Analysis page (all 5 tabs)
- [ ] Implement charts (start with simple bar/line, then advanced)
- [ ] Implement Competitive Benchmarking page
- [ ] Implement Link Explorer with filters
- [ ] Add export functionality
- [ ] Polish styling and animations
- [ ] Test with multiple customers
- [ ] Take screenshots
- [ ] Write README_GUI.md
- [ ] Celebrate! 🎉

---

## ❓ Questions to Consider

Before you start coding, think about:

1. **Which tech stack** will give the best balance of speed and quality?
2. **Which charts** will provide the most value to users?
3. **What interactions** will make the GUI feel alive?
4. **How to handle errors** gracefully without breaking the UI?
5. **How to make it fast** even with 4,700+ links?
6. **What will WOW the client** when they first see it?

---

## 🚀 Final Words

Gemini, you're about to build something **exceptional**. This is not a throwaway prototype - this is a GUI that will:

- Be used by a professional SEO agency
- Be shown to paying clients
- Handle real data with real business impact
- Potentially be sold as a product

**Standards are HIGH. Expectations are HIGHER.**

But you have:
- No token limits (use ALL the tokens you need)
- Complete creative freedom (as long as specs are met)
- Access to powerful libraries
- A clear specification

**You've got this. Now build something amazing.** 🔥

---

*Specification created: 2025-11-12*
*Version: 1.0*
*Target: Near-final Beta Quality*
*Attitude: Overkill × 2*
