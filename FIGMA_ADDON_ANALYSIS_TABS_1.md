# 📊 LinkDB Addon: Analysis Tabs Part 1

## 📋 Overview

This addon adds **2 professional analysis tabs** to the Customer Analysis page:
1. **Target URLs** - Deep linking analysis and URL distribution
2. **Link Velocity** - Link acquisition speed and trends over time

**⏱️ Estimated Time:** 25-35 minutes
**📦 Prerequisites:** Base design from `FIGMA_DESIGN_PROMPT.md` (Phases 1-15 completed)
**🎯 Outcome:** Two new analysis tabs with advanced visualizations

---

## 🎨 Design System Reference

Use the existing design system from `FIGMA_DESIGN_PROMPT.md`:

**Chart Colors:**
- Blue: #2563EB (light) / #3B82F6 (dark)
- Purple: #7C3AED (light) / #A78BFA (dark)
- Green: #059669 (light) / #10B981 (dark)
- Yellow: #D97706 (light) / #FBBF24 (dark)
- Red: #DC2626 (light) / #EF4444 (dark)

**Card Styling:**
- Background: white (light) / gray-800 (dark)
- Border: 1px solid gray-200/gray-700
- Border-radius: 12px
- Shadow: sm (0 1px 2px rgba(0,0,0,0.05))

**Typography:** Inter font family
**Spacing:** 8px base unit
**Grid:** 12 columns with 24px gap

---

## 🚀 Implementation Steps

### PART A: TARGET URLs TAB

---

### Step 1: Create Target URL Statistics Component

Navigate to **🧩 Components** page.

**Component: TargetURLStats**

1. Create frame: **Full width × 140px**
2. Apply **Auto Layout**:
   - Direction: Horizontal
   - Padding: 0
   - Gap: 24px
   - Alignment: Stretch

**Add 4 Stat Cards:**

Each card (width: 25%, Auto Layout vertical, gap 8px):

#### Stat Card 1: Total URLs
1. Frame: Quarter width × 140px
2. Background: white (light) / gray-800 (dark)
3. Border: 1px solid gray-200/gray-700
4. Border-radius: 12px
5. Padding: 24px

Content:
- **Label**: "Total URLs" (12px, uppercase, gray-500/gray-400)
- **Value**: "147" (36px, bold, gray-900/gray-100)
- **Icon**: 🔗 (24px, top-right corner)

#### Stat Card 2: Homepage Links
- Label: "Homepage Links"
- Value: "52"
- Subtext: "(35.4%)" (16px, blue-600/blue-400)
- Icon: 🏠

#### Stat Card 3: Deep Links
- Label: "Deep Links"
- Value: "95"
- Subtext: "(64.6%)" (16px, green-600/green-400)
- Icon: 📄

#### Stat Card 4: Diversity Score
- Label: "Diversity"
- Value: "78/100"
- Progress bar: 78% filled (blue-600/blue-500)
- Icon: 📊

---

### Step 2: Create Deep Linking Chart Component

Navigate to **🧩 Components** page.

**Component: DeepLinkingChart**

1. Create Card frame: **Full width × 400px**
2. Card title: "Deep Linking Distribution"

**Chart Area:**

1. **Donut Chart** (centered, 300×300px):
   - Use Figma's arc tool or plugin
   - Center hole: 120px diameter
   - Segments (clockwise from top):

     **Homepage - 35.4%**
     - Color: blue-600 (light) / blue-500 (dark)
     - Arc: 127 degrees

     **Category Pages - 28.3%**
     - Color: purple-600 (light) / purple-500 (dark)
     - Arc: 102 degrees

     **Blog Posts - 22.1%**
     - Color: green-600 (light) / green-500 (dark)
     - Arc: 80 degrees

     **Product Pages - 14.2%**
     - Color: yellow-500 (light) / yellow-400 (dark)
     - Arc: 51 degrees

2. **Center Text** (inside donut hole):
   - "147" (32px, bold, gray-900/gray-100)
   - "Total URLs" (14px, gray-600/gray-400)

3. **Legend** (right side):
   - Frame: 200px width × auto height
   - Auto Layout: Vertical, gap 12px
   - Position: Right of chart

   Each legend item (horizontal, gap 8px):
   - Color dot: 12px circle
   - Label: "Homepage" (14px, gray-700/gray-300)
   - Value: "52 (35.4%)" (14px, semibold, gray-900/gray-100)

---

### Step 3: Create Top Target URLs Table

Navigate to **🧩 Components** page.

**Component: TargetURLTableRow**

1. Create frame: **Full width × 64px**
2. Auto Layout: Horizontal, padding 12px 16px, gap 16px

**Columns:**

1. **Rank**:
   - Width: 60px
   - Text: "#1" (14px, gray-500/gray-400)

2. **Target URL**:
   - Width: Flexible (fill)
   - Text: "example.com/blog/seo-guide" (14px, blue-600/blue-400, underlined)
   - Truncate with ellipsis if too long

3. **Links**:
   - Width: 80px
   - Text: "18" (14px, semibold, gray-900/gray-100)

4. **Type**:
   - Width: 120px
   - Badge component instance
   - Text: "Blog Post" (12px)
   - Color-coded:
     - Homepage: blue
     - Blog Post: purple
     - Category: green
     - Product: yellow

5. **Bar Chart**:
   - Width: 120px
   - Progress bar visual (proportional to link count)
   - Fill: blue-600/blue-500

**Create variants for hover states**

#### Top Target URLs Card

**Component: TopTargetURLsCard**

1. Create Card frame
2. Title: "Top Target URLs"
3. Content:
   - Table header row
   - 10+ TargetURLTableRow instances
   - Pagination at bottom

---

### Step 4: Assemble Target URLs Tab

Navigate to **📱 Pages - Light Mode** → **Customer Analysis** page.

1. Add new tab to tab navigation: **"Target URLs"**
   - Position: After "Domain Quality" tab
   - Before "AI Assistant" tab

2. Create tab content area:
   - Auto Layout: Vertical, gap 24px
   - Padding: 32px

   **Add in order:**
   1. TargetURLStats component (full width)
   2. DeepLinkingChart component (full width)
   3. TopTargetURLsCard component (full width)

---

### PART B: LINK VELOCITY TAB

---

### Step 5: Create Velocity Metrics Component

Navigate to **🧩 Components** page.

**Component: VelocityMetrics**

Similar to TargetURLStats, but with 4 different metrics:

1. Create frame: **Full width × 140px**
2. Grid: 4 equal columns, gap 24px

**Metrics:**

#### Metric 1: Average per Month
- Label: "Avg/Month"
- Value: "24.5"
- Subtext: "links" (14px, gray-600/gray-400)
- Icon: 📈

#### Metric 2: Trend
- Label: "Trend"
- Value: "↗ Accelerating" (28px)
- Color: green-600/green-400 (for accelerating)
- Icon: 🚀

**Trend Options:**
- ↗ Accelerating (green)
- → Stable (blue)
- ↘ Decelerating (yellow)
- ↓ Declining (red)

#### Metric 3: Peak Month
- Label: "Peak Month"
- Value: "42"
- Subtext: "Mar '24" (14px, gray-600/gray-400)
- Icon: ⬆️

#### Metric 4: Low Month
- Label: "Low Month"
- Value: "8"
- Subtext: "Jan '24" (14px, gray-600/gray-400)
- Icon: ⬇️

---

### Step 6: Create Monthly Velocity Chart

Navigate to **🧩 Components** page.

**Component: MonthlyVelocityChart**

1. Create Card frame: **Full width × 450px**
2. Card title: "Monthly Link Velocity"

**Chart Area:**

Use Recharts specifications or create visual representation:

1. **Line Chart** (800×350px):
   - X-axis: Months (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
   - Y-axis: Link count (0, 10, 20, 30, 40, 50)

2. **Data Line**:
   - Color: blue-600 (light) / blue-400 (dark)
   - Stroke width: 3px
   - Smooth curve (monotone)
   - Data points with circles (6px diameter)

   Sample data points:
   - Jan: 8
   - Feb: 12
   - Mar: 42 (peak - highlighted)
   - Apr: 28
   - May: 32
   - Jun: 25
   - Jul: 18
   - Aug: 22
   - Sep: 35
   - Oct: 30
   - Nov: 26
   - Dec: 24

3. **Trend Line** (dotted):
   - Color: purple-400 (light) / purple-300 (dark)
   - Stroke: Dashed (4px dash, 4px gap)
   - Shows overall trend direction

4. **Grid Lines**:
   - Horizontal lines at each Y-axis interval
   - Color: gray-200 (light) / gray-700 (dark)
   - Stroke: 1px

5. **Axes**:
   - X-axis line: gray-300/gray-600, 2px
   - Y-axis line: gray-300/gray-600, 2px
   - Labels: 12px, gray-600/gray-400

6. **Annotations** (for significant points):
   - Peak marker at March:
     - Small banner: "Peak: 42 links"
     - Background: green-50/green-900/20
     - Border: green-500
     - Position: Above data point

7. **Hover Tooltip** (design state):
   - Background: gray-900 (light) / white (dark)
   - Padding: 8px 12px
   - Border-radius: 6px
   - Shadow: lg
   - Content:
     - Month: "March 2024"
     - Links: "42 links"
     - Change: "+50% from Feb"

---

### Step 7: Create Velocity Insights Component

Navigate to **🧩 Components** page.

**Component: VelocityInsights**

1. Create Card frame: **Full width × Auto height**
2. Card title: "Velocity Insights"
3. Auto Layout: Vertical, gap 12px, padding 24px

**Add Insight Items:**

Each insight (horizontal layout, gap 12px):

1. **Icon** (28px):
   - ✓ Success (green circle with checkmark)
   - ⚠ Warning (yellow triangle with exclamation)
   - ℹ Info (blue circle with i)
   - ✗ Error (red circle with x)

2. **Text** (14px, line-height 1.5):
   - Color matches icon

**Sample Insights:**

1. ✓ (green) "Steady growth over last 6 months (+15% average)"
2. ⚠ (yellow) "Peak activity in March (42 links) - campaign launch?"
3. ℹ (blue) "Lower activity in summer months (typical seasonal pattern)"
4. ✓ (green) "No unnatural spikes detected"
5. ℹ (blue) "Current velocity: 24.5 links/month (above industry average)"

**Styling:**
- Background: gray-50 (light) / gray-900 (dark)
- Border-left: 4px solid (color matches icon)
- Border-radius: 8px
- Padding: 16px

---

### Step 8: Assemble Link Velocity Tab

Navigate to **📱 Pages - Light Mode** → **Customer Analysis** page.

1. Add new tab to tab navigation: **"Link Velocity"**
   - Position: After "Target URLs" tab

2. Create tab content area:
   - Auto Layout: Vertical, gap 24px
   - Padding: 32px

   **Add in order:**
   1. VelocityMetrics component (full width)
   2. MonthlyVelocityChart component (full width)
   3. VelocityInsights component (full width)

---

### Step 9: Dark Mode Integration

Navigate to **🌙 Pages - Dark Mode** → **Customer Analysis** page.

1. Repeat Steps 4 and 8 for dark mode
2. Ensure all components use dark mode color variants:
   - Chart lines: Lighter colors for dark background
   - Grid lines: Darker (gray-700)
   - Card backgrounds: gray-800
   - Text: gray-100

3. Test chart readability in dark mode

---

### Step 10: Responsive Adjustments

#### Target URLs Tab (Tablet/Mobile)

**Tablet (768px):**
- Stats: 2×2 grid instead of 1×4
- Donut chart: Reduce to 250×250px
- Legend: Move below chart
- Table: Reduce bar chart column width

**Mobile (375px):**
- Stats: Stack vertically (1 column)
- Donut chart: 200×200px, center aligned
- Legend: Full width, 2 columns
- Table: Hide rank and bar chart columns

#### Link Velocity Tab (Tablet/Mobile)

**Tablet (768px):**
- Metrics: 2×2 grid
- Chart: Full width, 300px height
- Insights: Full width

**Mobile (375px):**
- Metrics: Stack vertically
- Chart: 280px width, allow horizontal scroll
- Simplify chart: Remove trend line, keep data line only
- Insights: Full width, smaller icons (20px)

---

### Step 11: Add Developer Annotations

Navigate to **📐 Specs & Annotations** page.

```
=================================
TARGET URLs TAB
=================================

API Endpoint:
GET /api/advanced/customers/{id}/target-url-analysis?from_date=YYYY-MM&to_date=YYYY-MM

Response Format:
{
  "success": true,
  "data": {
    "statistics": {
      "total_urls": 147,
      "homepage_links": 52,
      "deep_links": 95,
      "diversity_score": 78.0
    },
    "distribution": {
      "homepage": { "count": 52, "percentage": 35.4 },
      "category_pages": { "count": 42, "percentage": 28.6 },
      "blog_posts": { "count": 33, "percentage": 22.4 },
      "product_pages": { "count": 20, "percentage": 13.6 }
    },
    "top_urls": [
      {
        "target_url": "example.com/blog/seo-guide",
        "link_count": 18,
        "url_type": "blog_post"
      }
    ]
  }
}

Chart:
- Use Recharts PieChart component
- Set innerRadius for donut effect (60% of radius)
- Colors from design system
- Responsive: Reduce size on mobile

Insights:
- Deep linking ratio > 50% = Good (green)
- Deep linking ratio 30-50% = Medium (yellow)
- Deep linking ratio < 30% = Poor (red)

=================================
LINK VELOCITY TAB
=================================

API Endpoint:
GET /api/advanced/customers/{id}/link-velocity?from_date=YYYY-MM&to_date=YYYY-MM

Response Format:
{
  "success": true,
  "data": {
    "statistics": {
      "links_per_month": 24.5,
      "trend": "accelerating",
      "peak_month": "2024-03",
      "peak_count": 42,
      "low_month": "2024-01",
      "low_count": 8
    },
    "monthly_data": [
      { "month": "2024-01", "link_count": 8 },
      { "month": "2024-02", "link_count": 12 },
      { "month": "2024-03", "link_count": 42 }
    ],
    "insights": [
      {
        "type": "success",
        "message": "Steady growth over last 6 months (+15% average)"
      }
    ]
  }
}

Chart:
- Use Recharts LineChart component
- Data key: link_count
- Stroke: blue-600 (light) / blue-400 (dark)
- Add CartesianGrid for background grid
- Add Tooltip on hover
- Responsive: Reduce height on mobile

Trend Calculation:
- Accelerating: Last 3 months avg > Previous 3 months avg
- Stable: Within ±10% difference
- Decelerating: Last 3 months avg < Previous 3 months avg
- Declining: Negative trend over 6+ months

Insights Generation:
- Automatic based on data patterns
- Icons: ✓ (green), ⚠ (yellow), ℹ (blue), ✗ (red)
- Show 4-6 most relevant insights
```

---

### Step 12: Create Prototype Interactions

**Target URLs Tab:**
1. Click URL row → Show modal with all links to that URL
2. Hover donut segment → Highlight segment + show tooltip
3. Click legend item → Filter table to show only that type

**Link Velocity Tab:**
1. Hover chart point → Show tooltip with month details
2. Click peak marker → Show campaign analysis modal
3. Click insight → Expand with detailed explanation

---

## ✅ Implementation Checklist

**Target URLs Tab:**
- [ ] Create TargetURLStats component (4 metrics)
- [ ] Create DeepLinkingChart (donut chart)
- [ ] Create donut segments with correct percentages
- [ ] Create chart legend
- [ ] Create TargetURLTableRow component
- [ ] Create TopTargetURLsCard with table
- [ ] Assemble Target URLs tab content
- [ ] Test in light mode
- [ ] Test in dark mode
- [ ] Create responsive layouts

**Link Velocity Tab:**
- [ ] Create VelocityMetrics component (4 metrics)
- [ ] Create MonthlyVelocityChart (line chart)
- [ ] Add data points and trend line
- [ ] Add grid lines and axes
- [ ] Create hover tooltip design
- [ ] Create VelocityInsights component
- [ ] Add 4-6 insight items with icons
- [ ] Assemble Link Velocity tab content
- [ ] Test in light mode
- [ ] Test in dark mode
- [ ] Create responsive layouts

**Integration:**
- [ ] Add "Target URLs" tab to navigation
- [ ] Add "Link Velocity" tab to navigation
- [ ] Ensure tabs switch correctly
- [ ] Test with DateRangeFilter (if added)

**Documentation:**
- [ ] Add API endpoint annotations
- [ ] Document chart specifications
- [ ] Add responsive breakpoints
- [ ] Include calculation methods

---

## 🎯 Success Criteria

Your implementation is complete when:

1. ✅ Target URLs tab shows URL distribution with donut chart
2. ✅ Top target URLs table displays ranked URLs by link count
3. ✅ URL type badges are color-coded correctly
4. ✅ Link Velocity tab shows monthly trend line chart
5. ✅ Velocity metrics display average, trend, peak, and low
6. ✅ Insights panel shows 4-6 actionable insights
7. ✅ Both tabs work in light and dark modes
8. ✅ Responsive layouts work on all screen sizes
9. ✅ Charts use correct colors from design system
10. ✅ Developer annotations are comprehensive

---

## 📊 Visual Reference

```
TARGET URLs TAB:
┌────────────────────────────────────────────────────────────────┐
│ Total URLs: 147  │  Homepage: 52  │  Deep: 95  │  Score: 78   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│           ◉ Donut Chart              Legend:                   │
│          147 Total                   ● Homepage: 52 (35.4%)    │
│                                      ● Category: 42 (28.6%)    │
│                                      ● Blog: 33 (22.4%)        │
│                                      ● Product: 20 (13.6%)     │
├────────────────────────────────────────────────────────────────┤
│ #  │ URL                    │ Links │ Type       │ ████       │
│ 1  │ example.com/blog/...   │  18   │ Blog Post  │ ████████   │
│ 2  │ example.com/services   │  15   │ Category   │ ██████     │
└────────────────────────────────────────────────────────────────┘

LINK VELOCITY TAB:
┌────────────────────────────────────────────────────────────────┐
│ Avg: 24.5  │  ↗ Accelerating  │  Peak: 42  │  Low: 8         │
├────────────────────────────────────────────────────────────────┤
│ Links                                                           │
│ 50 │              ╭─Peak──╮                                    │
│ 40 │          ╭───╯       │                                    │
│ 30 │      ╭───╯           ╰──╮                                 │
│ 20 │  ╭───╯                  ╰─╮                               │
│ 10 │╭─╯                         ╰──                            │
│  0 └──────────────────────────────                             │
│    J  F  M  A  M  J  J  A  S  O  N  D                         │
├────────────────────────────────────────────────────────────────┤
│ ✓ Steady growth over last 6 months (+15% average)             │
│ ⚠ Peak activity in March (42 links) - campaign launch?        │
│ ℹ Lower activity in summer months (typical seasonal pattern)  │
└────────────────────────────────────────────────────────────────┘
```

---

**Version:** 1.0
**Estimated Time:** 25-35 minutes
**Difficulty:** ⭐⭐⭐ Intermediate-Advanced
**Dependencies:** FIGMA_DESIGN_PROMPT.md (Phases 1-15)
