# 🚀 LinkDB Advanced Features - Figma Design Update

## 📋 Overview

This prompt adds **advanced professional features** to the existing LinkDB Customer Analysis page design. These features transform LinkDB from a basic analytics tool into an enterprise-grade SEO platform.

**IMPORTANT:** This builds on top of the existing design from `FIGMA_DESIGN_PROMPT.md`. Use all existing design tokens, components, and styling.

---

## 🎯 New Backend Capabilities

### **1. Date Range Filtering** (Global)
All analysis tabs now support date filtering:
- From: Month/Year (YYYY-MM format)
- To: Month/Year (YYYY-MM format)
- Applies to ALL tabs simultaneously
- Persists across tab switches

### **2. Enhanced Anchor Analysis**
- Anchor text frequency (how many times each anchor is used)
- Word frequency in anchors (most used words)
- Search/filter for specific words in anchors
- Real-time statistics

### **3. New Analysis Tabs**
- Target URL Analysis
- Link Velocity & Trends
- Domain Sources
- Period Comparison
- Link Management (CRUD operations)

---

## 🎨 Design Updates

### **SECTION 1: Date Range Filter (New Component)**

Create a **global date range filter** that appears at the top of Customer Analysis page, below the Key Metrics cards.

#### **DateRangeFilter Component**

**Location:** Between "Key Metrics" and "Tabs" on Customer Analysis page

**Layout:** (Card component, full width)
```
Structure (Horizontal layout with Auto Layout):

[From Date]  [To Date]  [Apply]  [Clear]  [Date range indicator]

Components:
1. "From" Date Picker:
   - Label: "From" (12px, semibold, above input)
   - Input: Month/Year selector
   - Format shown: "Jan 2024" or "2024-01"
   - Width: 150px
   - Styling: Standard input component

2. Arrow Icon:
   - → (arrow right)
   - Color: gray-400
   - Size: 20px
   - Margin: 0 8px

3. "To" Date Picker:
   - Label: "To" (12px, semibold, above input)
   - Input: Month/Year selector
   - Format shown: "Dec 2024" or "2024-12"
   - Width: 150px
   - Styling: Standard input component

4. Apply Button:
   - Text: "Apply Filter"
   - Type: Primary button
   - Margin-left: 16px

5. Clear Button:
   - Text: "Clear"
   - Type: Secondary button
   - Margin-left: 8px

6. Active Filter Indicator (when filter is applied):
   - Background: blue-50 (light) / blue-900/20 (dark)
   - Border: 1px solid blue-200 (light) / blue-800 (dark)
   - Padding: 8px 12px
   - Border-radius: 6px
   - Text: "Showing: Jan 2024 - Dec 2024" (14px, blue-700/blue-400)
   - X icon to clear (16px, clickable)
   - Margin-left: auto (pushes to right)
```

**Visual Example:**
```
┌──────────────────────────────────────────────────────────────────┐
│  Filter by Date Range                                            │
│                                                                   │
│  From          To           Apply Filter  Clear   📅 Jan-Dec 2024│
│  [2024-01▾]  [2024-12▾]     [Button]     [Button]     [×]       │
└──────────────────────────────────────────────────────────────────┘
```

---

### **SECTION 2: Enhanced Anchor Analysis Tab**

Update the existing "Anchor Analysis" tab to include new sub-sections.

#### **2.1 Anchor Analysis Toolbar** (New)

Add a toolbar at the top of Anchor Analysis tab content:

**Layout:** (Horizontal, space-between)
```
Left side:
- Tab pills to switch views:
  [Distribution] [Frequency] [Word Cloud] [Search]

Right side:
- Export button (CSV icon)
- Settings icon (filter options)
```

**Tab Pills Design:**
```
Inactive:
- Background: transparent
- Text: gray-600 (light) / gray-400 (dark)
- Border-bottom: 2px transparent
- Padding: 8px 16px

Active:
- Background: blue-50 (light) / blue-900/20 (dark)
- Text: blue-600 (light) / blue-400 (dark)
- Border-bottom: 2px solid blue-600/blue-400
- Padding: 8px 16px
```

#### **2.2 Frequency View** (New Sub-tab)

When "Frequency" is selected, show:

**Card: "Anchor Text Frequency"**

**Table Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│  Rank  │  Anchor Text              │  Count  │  Percentage  │  █│
├─────────────────────────────────────────────────────────────────┤
│  1     │  best seo services        │  45     │  15.2%       │ ████│
│  2     │  professional seo         │  38     │  12.8%       │ ███│
│  3     │  click here               │  32     │  10.8%       │ ███│
│  4     │  ExampleBrand             │  28     │   9.5%       │ ██│
│  5     │  learn more               │  24     │   8.1%       │ ██│
│  ...                                                           │
└─────────────────────────────────────────────────────────────────┘

Table Features:
- Sortable columns (click header to sort)
- Visual bar chart in last column (proportional to percentage)
- Hover: highlight row
- Click row: show details modal (which links use this anchor)

Statistics Panel (above table):
- Total Links: 296
- Unique Anchors: 87
- Top anchor usage: 15.2%
- Diversity score: 72/100
```

#### **2.3 Word Cloud View** (New Sub-tab)

When "Word Cloud" is selected:

**Card: "Word Frequency in Anchors"**

**Layout:**
```
Top section (Controls):
- Min word length: [3▾] (dropdown: 1, 2, 3, 4, 5)
- Exclude common words: [✓] (checkbox)
- Show top: [100▾] words (dropdown: 50, 100, 200, 500)

Word Frequency Table:
┌────────────────────────────────────────────────────────┐
│  Word      │  Frequency  │  Used in X anchors  │  █   │
├────────────────────────────────────────────────────────┤
│  seo       │  145        │  67 anchors         │ █████│
│  services  │  89         │  42 anchors         │ ███  │
│  best      │  76         │  38 anchors         │ ███  │
│  professional│ 54        │  29 anchors         │ ██   │
│  marketing │  48         │  25 anchors         │ ██   │
└────────────────────────────────────────────────────────┘

Visual word cloud (optional):
- Words sized by frequency
- Color coded by category if applicable
- Interactive: click word to see which anchors contain it
```

#### **2.4 Search View** (New Sub-tab)

When "Search" is selected:

**Card: "Search Anchor Texts"**

**Layout:**
```
Search Bar:
┌─────────────────────────────────────────────────────────┐
│  🔍  [Search for word or phrase...]         [Search]   │
│                                                          │
│  ☐ Case sensitive                                       │
└─────────────────────────────────────────────────────────┘

Results (after search):
┌─────────────────────────────────────────────────────────┐
│  Found 23 links containing "seo services"               │
│                                                          │
│  Anchor Text           │  Pub Domain      │  Date       │
│  ─────────────────────────────────────────────────────  │
│  best seo services     │  example.com     │  2024-03-15 │
│  professional seo...   │  blog.site.com   │  2024-03-10 │
│  seo services expert   │  news.domain.io  │  2024-02-28 │
│  ...                                                     │
└─────────────────────────────────────────────────────────┘

Export button: "Export Results (CSV)"
```

---

### **SECTION 3: New Analysis Tabs**

Add these new tabs to the tab navigation (after existing tabs):

**Updated Tab List:**
1. Overview
2. Anchor Analysis ← (Enhanced)
3. Temporal Patterns
4. Domain Quality
5. **Target URLs** ← NEW
6. **Link Velocity** ← NEW
7. **Domain Sources** ← NEW
8. **Comparison** ← NEW
9. **Manage Links** ← NEW
10. 🤖 AI Assistant

---

#### **3.1 Target URLs Tab** (NEW)

**Purpose:** Shows which pages on the customer's site receive links.

**Layout:**

**Card 1: Target URL Statistics**
```
Grid (4 columns):
┌────────────────────────────────────────────────────────────────┐
│  Total URLs    │  Homepage Links  │  Deep Links  │  Diversity │
│  147           │  52 (35.4%)      │  95 (64.6%)  │  78/100    │
└────────────────────────────────────────────────────────────────┘
```

**Card 2: Deep Linking Visualization**
```
Pie Chart or Donut Chart:
- Homepage: 35.4% (blue)
- Category pages: 28.3% (purple)
- Blog posts: 22.1% (green)
- Product pages: 14.2% (yellow)

Legend on right side
```

**Card 3: Top Target URLs**
```
Table:
┌────────────────────────────────────────────────────────────────┐
│ Rank │ Target URL                    │ Links │ Type          │ █│
├────────────────────────────────────────────────────────────────┤
│  1   │ example.com/                  │  52   │ Homepage      │ ████│
│  2   │ example.com/blog/seo-guide    │  18   │ Blog Post     │ ██│
│  3   │ example.com/services          │  15   │ Category      │ █│
│  4   │ example.com/about-us          │  12   │ Page          │ █│
│  5   │ example.com/products/abc      │  10   │ Product       │ █│
│  ...                                                           │
└────────────────────────────────────────────────────────────────┘

Features:
- Click URL to filter links by that target
- Color coding by type
- Visual bar chart
```

---

#### **3.2 Link Velocity Tab** (NEW)

**Purpose:** Shows link acquisition speed and trends over time.

**Layout:**

**Card 1: Velocity Metrics**
```
Grid (4 columns):
┌────────────────────────────────────────────────────────────────┐
│  Avg/Month    │  Trend          │  Peak Month   │  Low Month  │
│  24.5 links   │  ↗ Accelerating │  42 (Mar'24)  │  8 (Jan'24) │
└────────────────────────────────────────────────────────────────┘

Trend indicator:
- ↗ Accelerating (green)
- → Stable (blue)
- ↘ Decelerating (yellow)
- ↓ Declining (red)
```

**Card 2: Monthly Velocity Chart**
```
Line Chart showing links per month:

   Links
   50 │        ╭────╮
   40 │    ╭───╯    │
   30 │  ╭─╯        ╰─╮
   20 │╭─╯            ╰─╮
   10 │╯                ╰──
    0 └─────────────────────
      J F M A M J J A S O N D

- X-axis: Months
- Y-axis: Link count
- Trend line overlay (dotted)
- Hover: show exact count
- Annotations for significant changes
```

**Card 3: Velocity Insights**
```
List of insights:
┌────────────────────────────────────────────────────────────────┐
│ ✓ Steady growth over last 6 months (+15% average)             │
│ ⚠ Peak activity in March (42 links) - campaign launch?        │
│ ℹ Lower activity in summer months (typical seasonal pattern)  │
│ ✓ No unnatural spikes detected                                │
└────────────────────────────────────────────────────────────────┘

Icons:
- ✓ = green (good)
- ⚠ = yellow (attention)
- ℹ = blue (info)
- ✗ = red (warning)
```

---

#### **3.3 Domain Sources Tab** (NEW)

**Purpose:** Analyzes which domains are providing links.

**Layout:**

**Card 1: Domain Statistics**
```
Grid (4 columns):
┌────────────────────────────────────────────────────────────────┐
│  Total Domains │  New Domains  │  Returning    │  Avg Links/Dom│
│  156           │  42 (26.9%)   │  114 (73.1%)  │  1.9          │
└────────────────────────────────────────────────────────────────┘
```

**Card 2: New vs Returning Domains Chart**
```
Stacked Bar Chart (monthly):

   Domains
   20 │ ████████████
      │ ████████████
   15 │ ████████████░░░░
      │ ████████████░░░░
   10 │ ████████████░░░░░░░░
      │ ████████████░░░░░░░░
    5 │ ████████████░░░░░░░░░░░░
      │ ████████████░░░░░░░░░░░░
    0 └─────────────────────────
      J F M A M J J A S O N D

Legend:
- ████ New domains (blue)
- ░░░░ Returning domains (purple)
```

**Card 3: Top Referring Domains**
```
Table:
┌────────────────────────────────────────────────────────────────┐
│ Domain              │ Links │ First Link │ Latest Link │ Status│
├────────────────────────────────────────────────────────────────┤
│ blog.example.com    │  8    │ 2023-05-12 │ 2024-03-10  │ ●RETURN│
│ news.site.io        │  6    │ 2024-01-08 │ 2024-03-15  │ ●RETURN│
│ forum.domain.com    │  1    │ 2024-03-18 │ 2024-03-18  │ ○NEW  │
│ article.web.org     │  4    │ 2023-11-20 │ 2024-02-14  │ ●RETURN│
└────────────────────────────────────────────────────────────────┘

Status badges:
- ●RETURN (blue) = multiple links over time
- ○NEW (green) = first link
```

---

#### **3.4 Comparison Tab** (NEW)

**Purpose:** Compare two time periods (before/after campaigns, month-over-month, etc.)

**Layout:**

**Card 1: Period Selection**
```
┌────────────────────────────────────────────────────────────────┐
│  Compare Two Periods                                           │
│                                                                 │
│  Period 1:  [2024-01] to [2024-03]   (3 months)               │
│  Period 2:  [2024-04] to [2024-06]   (3 months)               │
│                                                                 │
│  [Compare] [Quick Select: Q1 vs Q2▾]                          │
└────────────────────────────────────────────────────────────────┘

Quick Select dropdown:
- Month vs Month
- Quarter vs Quarter
- Last 3 months vs Previous 3 months
- Custom (manual selection)
```

**Card 2: Comparison Results**
```
Side-by-side comparison:

┌─────────────────────────────────────────────────────────────────┐
│                 Period 1        Period 2        Change          │
│                 (Jan-Mar)       (Apr-Jun)                       │
├─────────────────────────────────────────────────────────────────┤
│ Total Links     72             95              +23 (+31.9%) ↗  │
│ Unique Domains  34             48              +14 (+41.2%) ↗  │
│ Target URLs     18             22              +4  (+22.2%) ↗  │
│ New Domains     12             19              +7  (+58.3%) ↗  │
└─────────────────────────────────────────────────────────────────┘

Change indicators:
- ↗ = green (positive growth)
- → = blue (stable)
- ↘ = yellow (slight decrease)
- ↓ = red (significant decrease)
```

**Card 3: Visual Comparison**
```
Bar Chart comparing metrics side-by-side:

   Links
   100│         ██
      │         ██
    75│         ██
      │    ██   ██
    50│    ██   ██
      │    ██   ██
    25│    ██   ██
      │    ██   ██
     0└────────────
         P1   P2

- Blue bars = Period 1
- Purple bars = Period 2
- Multiple metrics shown (links, domains, etc.)
```

---

#### **3.5 Manage Links Tab** (NEW)

**Purpose:** CRUD operations - Create, Read, Update, Delete links.

**Layout:**

**Toolbar:**
```
┌────────────────────────────────────────────────────────────────┐
│ [+ Add New Link]  [🔍 Search]  [Filter▾]  [Sort▾]  [Delete Selected] │
└────────────────────────────────────────────────────────────────┘
```

**Table:** (Editable)
```
┌────────────────────────────────────────────────────────────────────────┐
│ ☐│ID│ Pub Domain    │ Target URL    │ Anchor Text   │ Date     │ Actions│
├────────────────────────────────────────────────────────────────────────┤
│ ☐│1 │example.com    │site.com/about │learn more     │2024-03-15│ ✏️ 🗑️│
│ ☐│2 │blog.site.io   │site.com/blog  │best seo guide │2024-03-10│ ✏️ 🗑️│
│ ☐│3 │news.web.com   │site.com/      │click here     │2024-02-28│ ✏️ 🗑️│
└────────────────────────────────────────────────────────────────────────┘

Features:
- Checkbox: Select multiple for bulk operations
- ✏️ Edit icon: Opens edit modal
- 🗑️ Delete icon: Confirm and delete
- Click row: Show details view
- Inline editing (double-click cell)
```

**Add/Edit Modal:**
```
┌──────────────────────────────────────────┐
│  ✕                Add New Link            │
├──────────────────────────────────────────┤
│                                           │
│  Publishing Domain *                      │
│  [_____________________________]          │
│                                           │
│  Target URL *                             │
│  [_____________________________]          │
│                                           │
│  Anchor Text *                            │
│  [_____________________________]          │
│                                           │
│  Published Date * (YYYY-MM-DD)            │
│  [2024-03-15]  [📅]                       │
│                                           │
│  [Cancel]  [Save Link]                    │
└──────────────────────────────────────────┘

Validation:
- Required fields marked with *
- Real-time validation
- Error messages below fields
- Success toast after save
```

**Bulk Actions:**
```
When items are selected:
┌────────────────────────────────────────────────────────────────┐
│ ✓ 3 links selected   [Bulk Edit]  [Export Selected]  [Delete] │
└────────────────────────────────────────────────────────────────┘

Delete Confirmation:
┌──────────────────────────────────────────┐
│  ⚠️  Delete 3 Links?                     │
├──────────────────────────────────────────┤
│  This action cannot be undone.           │
│  Are you sure you want to delete         │
│  these 3 links?                           │
│                                           │
│  [Cancel]  [Delete Permanently]          │
└──────────────────────────────────────────┘
```

---

## 🎨 Component Specifications

### **Date Picker Component** (NEW)

For Month/Year selection:

```
Design:
┌──────────────┐
│  2024-03  ▾  │
└──────────────┘

On click, dropdown opens:
┌──────────────┐
│  2024    ◄ ► │  ← Year selector with arrows
├──────────────┤
│  Jan  Feb  Mar│  ← Month grid (3x4)
│  Apr  May  Jun│
│  Jul  Aug  Sep│
│  Oct  Nov  Dec│
└──────────────┘

Styling:
- Input: Standard input component
- Dropdown: white/gray-800 background
- Selected month: blue-600/blue-400 background
- Hover: gray-100/gray-700 background
- Border-radius: 8px
- Shadow: md
```

### **Edit Modal Component** (NEW)

Standard modal for editing:

```
Backdrop: rgba(0, 0, 0, 0.5)
Modal:
- Width: 500px
- Max-height: 80vh
- Background: white (light) / gray-800 (dark)
- Border-radius: 12px
- Shadow: xl
- Padding: 24px
- Position: center screen

Header:
- Title: 20px, semibold
- Close X: top-right, 24px, clickable

Form:
- Labels: 14px, semibold, gray-700/gray-300
- Inputs: Standard input component
- Spacing: 16px between fields

Footer:
- Buttons: Right-aligned, 8px gap
- Cancel: Secondary button
- Save: Primary button
```

### **Statistics Panel Component** (NEW)

For showing metrics above tables/charts:

```
Design:
┌────────────────────────────────────────────────────────────────┐
│  📊 Statistics                                                 │
│                                                                 │
│  Total: 296  │  Unique: 87  │  Average: 3.4  │  Top: 15.2%   │
└────────────────────────────────────────────────────────────────┘

Styling:
- Background: gray-50 (light) / gray-900 (dark)
- Border: 1px solid gray-200/gray-700
- Border-radius: 8px
- Padding: 16px
- Display: flex, space-evenly
- Each stat:
  - Label: 12px, uppercase, gray-500/gray-400
  - Value: 20px, bold, gray-900/gray-100
```

---

## 📊 Chart Updates

### **Velocity Line Chart** (NEW)

Use Recharts LineChart:

```javascript
<LineChart data={monthlyData}>
  <Line
    type="monotone"
    dataKey="link_count"
    stroke="#3B82F6"  // blue-600
    strokeWidth={2}
    dot={{ fill: '#3B82F6', r: 4 }}
  />
  <XAxis dataKey="month" stroke="#9CA3AF" />
  <YAxis stroke="#9CA3AF" />
  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
  <Tooltip />
</LineChart>

Dark mode adjustments:
- Grid: #374151 (gray-700)
- Axis: #6B7280 (gray-500)
- Line: #60A5FA (blue-400)
```

### **Stacked Bar Chart** (NEW)

For domain sources:

```javascript
<BarChart data={monthlyData}>
  <Bar dataKey="new_domains" stackId="a" fill="#3B82F6" />
  <Bar dataKey="returning_domains" stackId="a" fill="#8B5CF6" />
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip />
  <Legend />
</BarChart>

Colors:
- New domains: blue-600 / blue-500
- Returning domains: purple-600 / purple-500
```

---

## ✅ Implementation Checklist

When implementing in Figma:

**Date Range Filter:**
- [ ] Create DateRangeFilter component
- [ ] Add to Customer Analysis page
- [ ] Create date picker component
- [ ] Add active filter indicator
- [ ] Test in both light and dark modes

**Enhanced Anchor Analysis:**
- [ ] Add toolbar with tab pills
- [ ] Create Frequency view table
- [ ] Create Word Cloud view
- [ ] Create Search view
- [ ] Add export buttons

**New Tabs:**
- [ ] Add 5 new tabs to navigation
- [ ] Create Target URLs tab content
- [ ] Create Link Velocity tab with line chart
- [ ] Create Domain Sources tab with stacked chart
- [ ] Create Comparison tab with side-by-side view
- [ ] Create Manage Links tab with editable table

**New Components:**
- [ ] Date picker (month/year)
- [ ] Edit modal
- [ ] Statistics panel
- [ ] Editable table
- [ ] Bulk action toolbar
- [ ] Confirmation dialogs

**Charts:**
- [ ] Line chart for velocity
- [ ] Stacked bar chart for domains
- [ ] Comparison bar chart
- [ ] Update color schemes for dark mode

**Responsive:**
- [ ] Test all new components on tablet
- [ ] Test all new components on mobile
- [ ] Ensure tables are scrollable
- [ ] Ensure modals are responsive

---

## 🎯 Success Criteria

The design is complete when:

1. ✅ Date range filter is visible and functional-looking on all analysis pages
2. ✅ Anchor Analysis has 4 sub-views (Distribution, Frequency, Word Cloud, Search)
3. ✅ All 5 new tabs are designed with complete layouts
4. ✅ CRUD operations are clearly shown in Manage Links tab
5. ✅ All new charts follow the existing chart design system
6. ✅ Edit modal and confirmations are professional
7. ✅ Dark mode works for all new components
8. ✅ Responsive layouts work on all screen sizes

---

## 📝 Developer Notes to Add

Add these annotations in Figma:

```
Date Range Filter:
- API: GET /api/advanced/customers/{id}/...?from_date=2024-01&to_date=2024-12
- Format: YYYY-MM
- Applies to all analysis endpoints

Anchor Frequency:
- Endpoint: /api/advanced/customers/{id}/anchor-frequency
- Params: from_date, to_date, limit

Word Frequency:
- Endpoint: /api/advanced/customers/{id}/word-frequency
- Params: from_date, to_date, min_length, limit

Search Anchors:
- Endpoint: /api/advanced/customers/{id}/anchor-search
- Params: search_term, from_date, to_date, case_sensitive

Target URL Analysis:
- Endpoint: /api/advanced/customers/{id}/target-url-analysis
- Shows deep linking ratio

Link Velocity:
- Endpoint: /api/advanced/customers/{id}/link-velocity
- Returns monthly data + trend

Domain Sources:
- Endpoint: /api/advanced/customers/{id}/domain-sources
- Shows new vs returning domains

Comparison:
- Endpoint: /api/advanced/customers/{id}/comparison
- Params: period1_from, period1_to, period2_from, period2_to

CRUD Operations:
- POST   /api/links/        - Create
- GET    /api/links/{id}    - Read
- PUT    /api/links/{id}    - Update
- DELETE /api/links/{id}    - Delete
- POST   /api/links/bulk-delete - Bulk delete
```

---

## 🚀 Ready to Implement

You now have complete specifications for:
- ✅ Date range filtering (global)
- ✅ Enhanced anchor analysis (4 views)
- ✅ 5 new analysis tabs
- ✅ CRUD functionality
- ✅ All necessary components
- ✅ Chart specifications
- ✅ Responsive considerations

**Next steps:**
1. Implement these designs in Figma using the existing design system
2. Create prototypes for interactive elements
3. Export specifications for developers
4. Frontend team implements using these exact designs

---

**Version:** 1.0
**Date:** 2025-11-12
**Dependencies:** Requires FIGMA_DESIGN_PROMPT.md base design system
