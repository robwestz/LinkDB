# 🎯 LinkDB Addon: Enhanced Anchor Analysis

## 📋 Overview

This addon transforms the basic **Anchor Analysis** tab into a professional SEO analysis tool with **4 specialized views**: Distribution, Frequency, Word Cloud, and Search.

**⏱️ Estimated Time:** 25-35 minutes
**📦 Prerequisites:** Base design from `FIGMA_DESIGN_PROMPT.md` (Phases 1-15 completed)
**🎯 Outcome:** Multi-view anchor analysis with advanced filtering and insights

---

## 🎨 Design System Reference

Use the existing design system from `FIGMA_DESIGN_PROMPT.md`:

**Colors (Light Mode):**
- Primary Blue: #2563EB (blue-600)
- Purple: #7C3AED (purple-600)
- Green: #059669 (green-600)
- Card: #FFFFFF (white)
- Background: #F9FAFB (gray-50)
- Text: #111827 (gray-900)

**Colors (Dark Mode):**
- Primary Blue: #3B82F6 (blue-500)
- Purple: #A78BFA (purple-400)
- Green: #10B981 (green-400)
- Card: #1F2937 (gray-800)
- Background: #111827 (gray-900)
- Text: #F9FAFB (gray-50)

**Typography:** Inter font, standard weights (400, 500, 600, 700)
**Spacing:** 8px base unit
**Border-radius:** 8px (standard), 12px (cards)

---

## 🚀 Implementation Steps

### Step 1: Create Tab Pills Component

Navigate to **🧩 Components** page.

#### 1.1 Single Tab Pill

**Component: TabPill**

1. Create frame: **Auto width × 40px height**
2. Apply **Auto Layout**:
   - Direction: Horizontal
   - Padding: 8px 16px
   - Gap: 4px
   - Alignment: Center

3. Add **Text**: "Distribution"
   - Font: Inter, 14px, Medium (500)

4. Add **Border-bottom**: 2px solid

**Create 2 Variants:**

**Variant 1: Inactive**
- Background: transparent
- Text color: gray-600 (light) / gray-400 (dark)
- Border-bottom: transparent

**Variant 2: Active**
- Background: blue-50 (light) / rgba(59, 130, 246, 0.1) (dark)
- Text color: blue-600 (light) / blue-400 (dark)
- Border-bottom: blue-600 (light) / blue-400 (dark)

#### 1.2 Tab Pills Group

**Component: AnchorAnalysisTabPills**

1. Create frame: **Auto width × 56px height**
2. Apply **Auto Layout**:
   - Direction: Horizontal
   - Padding: 8px 0
   - Gap: 4px
   - Alignment: Center

3. Add **4 TabPill instances**:
   - Distribution (Active by default)
   - Frequency
   - Word Cloud
   - Search

---

### Step 2: Create Toolbar Component

Navigate to **🧩 Components** page.

**Component: AnchorAnalysisToolbar**

1. Create frame: **Full width × 64px height**
2. Background: white (light) / gray-800 (dark)
3. Border-bottom: 1px solid gray-200 (light) / gray-700 (dark)
4. Apply **Auto Layout**:
   - Direction: Horizontal
   - Padding: 12px 24px
   - Justify: Space between
   - Alignment: Center

**Left Section:**
- Add instance of AnchorAnalysisTabPills

**Right Section:**
- Create frame (Auto Layout, horizontal, gap 8px)

  1. **Export Button**:
     - Instance of Button (Ghost variant)
     - Icon: 📊 or CSV icon
     - Text: "Export"
     - Width: 100px

  2. **Settings Icon**:
     - Circle: 36px diameter
     - Background: transparent
     - Hover: gray-100 (light) / gray-700 (dark)
     - Icon: ⚙️ (settings)
     - Size: 20px
     - Color: gray-600 (light) / gray-400 (dark)

---

### Step 3: Create Statistics Panel Component

Navigate to **🧩 Components** page.

**Component: StatisticsPanel**

1. Create frame: **Full width × 80px height**
2. Background: gray-50 (light) / gray-900 (dark)
3. Border: 1px solid gray-200 (light) / gray-700 (dark)
4. Border-radius: 8px
5. Apply **Auto Layout**:
   - Direction: Horizontal
   - Padding: 16px
   - Justify: Space evenly
   - Alignment: Center

**Add 4 Stat Items:**

Each stat item (vertical Auto Layout, gap 4px):

1. **Total Links**:
   - Label: "TOTAL LINKS" (12px, uppercase, gray-500)
   - Value: "296" (24px, bold, gray-900/gray-100)

2. **Unique Anchors**:
   - Label: "UNIQUE ANCHORS" (12px, uppercase, gray-500)
   - Value: "87" (24px, bold, gray-900/gray-100)

3. **Top Usage**:
   - Label: "TOP ANCHOR" (12px, uppercase, gray-500)
   - Value: "15.2%" (24px, bold, blue-600/blue-400)

4. **Diversity Score**:
   - Label: "DIVERSITY" (12px, uppercase, gray-500)
   - Value: "72/100" (24px, bold, green-600/green-400)

---

### Step 4: Create Frequency View

Navigate to **🧩 Components** page.

#### 4.1 Frequency Table Row

**Component: FrequencyTableRow**

1. Create frame: **Full width × 56px height**
2. Apply **Auto Layout**:
   - Direction: Horizontal
   - Padding: 12px 16px
   - Gap: 16px
   - Alignment: Center

3. Add columns:

   **Column 1: Rank**
   - Width: 60px
   - Text: "#1"
   - Font: Inter, 14px, Medium
   - Color: gray-500 (light) / gray-400 (dark)

   **Column 2: Anchor Text**
   - Width: Flexible (fill)
   - Text: "best seo services"
   - Font: Inter, 14px, Medium
   - Color: gray-900 (light) / gray-100 (dark)

   **Column 3: Count**
   - Width: 80px
   - Text: "45"
   - Font: Inter, 14px, Semibold
   - Color: gray-900 (light) / gray-100 (dark)

   **Column 4: Percentage**
   - Width: 100px
   - Text: "15.2%"
   - Font: Inter, 14px, Medium
   - Color: blue-600 (light) / blue-400 (dark)

   **Column 5: Bar Chart**
   - Width: 120px
   - Progress bar:
       - Background: gray-200 (light) / gray-700 (dark)
       - Fill: blue-600 (light) / blue-500 (dark)
       - Height: 8px
       - Border-radius: 4px
       - Width: Proportional to percentage

**Create Variants:**
- Light / Default
- Light / Hover (background: gray-50)
- Dark / Default
- Dark / Hover (background: gray-800)

#### 4.2 Frequency View Card

**Component: FrequencyView**

1. Create Card frame (standard card component)
2. Title: "Anchor Text Frequency"
3. Add **Auto Layout** (vertical, gap 16px):

   1. **StatisticsPanel** instance

   2. **Table Header**:
      - Frame: Full width × 40px
      - Background: gray-100 (light) / gray-800 (dark)
      - Auto Layout: Horizontal, padding 12px 16px, gap 16px

      - Columns (matching FrequencyTableRow):
        - "Rank" (60px, 12px, uppercase, semibold, gray-700/gray-300)
        - "Anchor Text" (Flexible, 12px, uppercase, semibold, gray-700/gray-300)
        - "Count" (80px, 12px, uppercase, semibold, gray-700/gray-300)
        - "Percentage" (100px, 12px, uppercase, semibold, gray-700/gray-300)
        - "Distribution" (120px, 12px, uppercase, semibold, gray-700/gray-300)

   3. **Table Rows** (10 instances of FrequencyTableRow):
      - Row 1: #1, "best seo services", 45, 15.2%, [full bar]
      - Row 2: #2, "professional seo", 38, 12.8%, [85% bar]
      - Row 3: #3, "click here", 32, 10.8%, [71% bar]
      - Row 4: #4, "ExampleBrand", 28, 9.5%, [63% bar]
      - Row 5: #5, "learn more", 24, 8.1%, [53% bar]
      - Rows 6-10: Decreasing values

   4. **Pagination**:
      - Frame: Full width × 48px
      - Auto Layout: Horizontal, space-between, padding 12px 16px

      - Left: "Showing 1-10 of 87" (14px, gray-600/gray-400)
      - Right: [Previous] [1] [2] [3] ... [9] [Next] buttons

---

### Step 5: Create Word Cloud View

Navigate to **🧩 Components** page.

#### 5.1 Word Cloud Controls

**Component: WordCloudControls**

1. Create frame: **Full width × 80px**
2. Background: gray-50 (light) / gray-900 (dark)
3. Border-radius: 8px
4. Padding: 16px
5. Auto Layout: Horizontal, gap 24px

**Add 3 Controls:**

1. **Min Word Length**:
   - Label: "Min length" (14px, gray-700/gray-300)
   - Dropdown: Instance of Select component
   - Options: [1, 2, 3, 4, 5]
   - Default: 3

2. **Exclude Common Words**:
   - Checkbox: ✓
   - Label: "Exclude common words" (14px, gray-700/gray-300)

3. **Show Top N**:
   - Label: "Show top" (14px, gray-700/gray-300)
   - Dropdown: Instance of Select component
   - Options: [50, 100, 200, 500]
   - Default: 100

#### 5.2 Word Frequency Table

**Component: WordFrequencyRow**

Similar to FrequencyTableRow, but with different columns:

1. Create frame: **Full width × 56px height**
2. Auto Layout: Horizontal, padding 12px 16px, gap 16px

**Columns:**
- **Word**: "seo" (Flexible width, bold)
- **Frequency**: "145" (80px, semibold)
- **In X Anchors**: "67 anchors" (120px, gray-600/gray-400)
- **Bar Chart**: Visual representation (120px)

#### 5.3 Word Cloud View Card

**Component: WordCloudView**

1. Create Card frame
2. Title: "Word Frequency in Anchors"
3. Auto Layout: Vertical, gap 16px

   1. **WordCloudControls** instance

   2. **Table** (similar structure to Frequency View):
      - Header row
      - 10+ WordFrequencyRow instances
      - Top words: "seo", "services", "best", "professional", "marketing", etc.

   3. **Optional Visual Word Cloud** (decorative):
      - Frame: Full width × 300px
      - Words arranged artistically
      - Font sizes: 12px to 48px based on frequency
      - Colors: Mix of blue, purple, green shades
      - Interactive hover states

---

### Step 6: Create Search View

Navigate to **🧩 Components** page.

#### 6.1 Search Bar

**Component: AnchorSearchBar**

1. Create frame: **Full width × 120px**
2. Background: white (light) / gray-800 (dark)
3. Border: 1px solid gray-200 (light) / gray-700 (dark)
4. Border-radius: 12px
5. Padding: 24px
6. Auto Layout: Vertical, gap 16px

**Search Input:**
1. Frame: Full width × 48px
   - Auto Layout: Horizontal, padding 12px 16px, gap 12px
   - Background: gray-50 (light) / gray-900 (dark)
   - Border: 1px solid gray-300 (light) / gray-600 (dark)
   - Border-radius: 8px

   - **Icon**: 🔍 (20px, gray-400)
   - **Input Text**: "Search for word or phrase..." (14px, gray-500)
   - **Search Button**: Instance of Button (Primary)

**Checkbox:**
- ☐ Case sensitive (14px, gray-700/gray-300)

#### 6.2 Search Results Row

**Component: SearchResultRow**

1. Create frame: **Full width × 64px**
2. Auto Layout: Horizontal, padding 12px 16px, gap 16px
3. Background: Hover state gray-50/gray-800

**Columns:**
- **Anchor Text**: "best seo services" (Flexible, bold)
- **Pub Domain**: "example.com" (200px, gray-600/gray-400)
- **Date**: "2024-03-15" (120px, gray-600/gray-400)
- **View Icon**: → (20px, blue-600/blue-400)

#### 6.3 Search View Card

**Component: SearchView**

1. Create Card frame
2. Title: "Search Anchor Texts"
3. Auto Layout: Vertical, gap 16px

   1. **AnchorSearchBar** instance

   2. **Results Header**:
      - Frame: Full width × 48px
      - Background: blue-50 (light) / blue-900/20 (dark)
      - Padding: 12px 16px
      - Text: "Found 23 links containing 'seo services'" (14px, blue-700/blue-300)

   3. **Results Table**:
      - Header row (columns: Anchor Text, Pub Domain, Date)
      - 10 SearchResultRow instances
      - Alternate row backgrounds for readability

   4. **Export Button**:
      - Instance of Button (Secondary)
      - Text: "Export Results (CSV)"
      - Icon: 📊
      - Aligned right

---

### Step 7: Update Anchor Analysis Tab

Navigate to **📱 Pages - Light Mode** → **Customer Analysis** page.

#### 7.1 Add Toolbar

1. Find the **Anchor Analysis** tab content
2. At the top, add **AnchorAnalysisToolbar** instance
3. Position: Full width, directly below tab navigation
4. Z-index: Ensure it's above content

#### 7.2 Create 4 Tab Content Views

Create **4 versions** of the Anchor Analysis tab:

**Version 1: Distribution (Default)**
- Keep existing anchor distribution content
- Add StatisticsPanel at top

**Version 2: Frequency**
- Replace content with FrequencyView component
- Full width, standard spacing

**Version 3: Word Cloud**
- Replace content with WordCloudView component
- Full width, standard spacing

**Version 4: Search**
- Replace content with SearchView component
- Full width, standard spacing

---

### Step 8: Dark Mode Integration

Navigate to **🌙 Pages - Dark Mode** → **Customer Analysis** page.

1. Repeat Step 7 for dark mode
2. Ensure all component variants use dark mode versions
3. Test all 4 tab views in dark mode

---

### Step 9: Responsive Adjustments

#### 9.1 Tablet Layout (768px)

**Toolbar:**
- Stack Export button below tab pills on tablet
- Settings icon stays on right

**Tables:**
- Reduce bar chart column width to 80px
- Make anchor text column flexible
- Allow horizontal scroll if needed

**Word Cloud:**
- Reduce visual cloud height to 200px
- Stack controls vertically

#### 9.2 Mobile Layout (375px)

**Toolbar:**
- Tab pills: Scroll horizontally
- Export/Settings: Move to dropdown menu (☰)

**Tables:**
- Show only: Anchor Text + Count
- Hide: Rank, Percentage, Bar chart
- Tap row to see details modal

**Search:**
- Full width search input
- Stack checkbox below search
- Results: Show only anchor + domain

---

### Step 10: Add Developer Annotations

Navigate to **📐 Specs & Annotations** page.

```
=================================
ENHANCED ANCHOR ANALYSIS
=================================

API Endpoints:
1. Frequency View:
   GET /api/advanced/customers/{id}/anchor-frequency
   Params: ?from_date=YYYY-MM&to_date=YYYY-MM&limit=100

2. Word Cloud View:
   GET /api/advanced/customers/{id}/word-frequency
   Params: ?from_date=YYYY-MM&to_date=YYYY-MM&min_length=3&limit=100

3. Search View:
   GET /api/advanced/customers/{id}/anchor-search
   Params: ?search_term=seo&from_date=YYYY-MM&to_date=YYYY-MM&case_sensitive=false

Response Format (Frequency):
{
  "success": true,
  "data": {
    "anchors": [
      {
        "anchor_text": "best seo services",
        "frequency": 45,
        "percentage": 15.2
      }
    ],
    "statistics": {
      "total_links": 296,
      "unique_anchors": 87,
      "diversity_score": 72.0
    }
  }
}

Tab Switching:
- Use React state to track active tab
- Only render active view (performance)
- Persist tab selection in URL (?view=frequency)

Export Functionality:
- Generate CSV from current view data
- Columns: All visible columns + date
- Filename: "anchors-frequency-2024-03-15.csv"

Search:
- Client-side filtering for instant results
- Server-side for large datasets
- Debounce search input (300ms)

Pagination:
- 10 rows per page (default)
- Options: 10, 25, 50, 100
- Server-side pagination for large datasets
```

---

### Step 11: Create Prototype Interactions

**Tab Switching:**
- On click "Frequency" tab → Navigate to Frequency view
- On click "Word Cloud" tab → Navigate to Word Cloud view
- On click "Search" tab → Navigate to Search view
- Animation: Fade (200ms)

**Table Interactions:**
- On hover row → Show hover state
- On click row → Open detail modal (show all links with this anchor)

**Search:**
- On type in search → Show loading state
- On click Search button → Show results

---

## ✅ Implementation Checklist

**Components:**
- [ ] Create TabPill component with 2 variants
- [ ] Create AnchorAnalysisTabPills with 4 tabs
- [ ] Create AnchorAnalysisToolbar
- [ ] Create StatisticsPanel component
- [ ] Create FrequencyTableRow component
- [ ] Create FrequencyView card
- [ ] Create WordCloudControls
- [ ] Create WordFrequencyRow
- [ ] Create WordCloudView card
- [ ] Create AnchorSearchBar
- [ ] Create SearchResultRow
- [ ] Create SearchView card

**Page Integration:**
- [ ] Add toolbar to Anchor Analysis tab
- [ ] Create Distribution view (enhanced existing)
- [ ] Create Frequency view
- [ ] Create Word Cloud view
- [ ] Create Search view
- [ ] Test all 4 views in light mode
- [ ] Test all 4 views in dark mode

**Responsive:**
- [ ] Tablet: Adjust toolbar layout
- [ ] Tablet: Optimize table columns
- [ ] Mobile: Horizontal scroll for tabs
- [ ] Mobile: Simplified table columns
- [ ] Test all views on all breakpoints

**Prototyping:**
- [ ] Add tab switching interactions
- [ ] Add table row hover/click
- [ ] Add search interactions
- [ ] Add export button interaction

**Documentation:**
- [ ] Add API endpoint annotations
- [ ] Document tab switching logic
- [ ] Add export functionality notes
- [ ] Include pagination specs

---

## 🎯 Success Criteria

Your implementation is complete when:

1. ✅ Toolbar with 4 tab pills appears at top of Anchor Analysis
2. ✅ All 4 views (Distribution, Frequency, Word Cloud, Search) are designed
3. ✅ StatisticsPanel shows key metrics in all views
4. ✅ Frequency table displays ranked anchor texts with visual bars
5. ✅ Word Cloud view shows word analysis with controls
6. ✅ Search view has functional-looking search bar and results
7. ✅ All components work in both light and dark modes
8. ✅ Responsive layouts work on all screen sizes
9. ✅ Prototype demonstrates tab switching
10. ✅ Developer annotations are comprehensive

---

## 📊 Visual Reference

```
TOOLBAR:
┌────────────────────────────────────────────────────────────────┐
│ [Distribution] [Frequency] [Word Cloud] [Search]   📊 Export ⚙️│
└────────────────────────────────────────────────────────────────┘

FREQUENCY VIEW:
┌────────────────────────────────────────────────────────────────┐
│ TOTAL: 296  │  UNIQUE: 87  │  TOP: 15.2%  │  DIVERSITY: 72   │
├────────────────────────────────────────────────────────────────┤
│ Rank │ Anchor Text          │ Count │ %     │ ████████        │
│  #1  │ best seo services    │  45   │ 15.2% │ ████████████    │
│  #2  │ professional seo     │  38   │ 12.8% │ ██████████      │
│  #3  │ click here           │  32   │ 10.8% │ ████████        │
└────────────────────────────────────────────────────────────────┘
```

---

**Version:** 1.0
**Estimated Time:** 25-35 minutes
**Difficulty:** ⭐⭐⭐ Intermediate-Advanced
**Dependencies:** FIGMA_DESIGN_PROMPT.md (Phases 1-15)
