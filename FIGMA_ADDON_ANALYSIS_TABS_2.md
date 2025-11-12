# 🔧 LinkDB Addon: Analysis Tabs Part 2 + CRUD

## 📋 Overview

This addon adds **3 advanced tabs** to the Customer Analysis page:
1. **Domain Sources** - Track new vs returning domains over time
2. **Comparison** - Compare two time periods side-by-side
3. **Manage Links** - Full CRUD interface for link management

**⏱️ Estimated Time:** 30-40 minutes
**📦 Prerequisites:** Base design from `FIGMA_DESIGN_PROMPT.md` (Phases 1-15 completed)
**🎯 Outcome:** Three feature-rich tabs with professional UI

---

## 🎨 Design System Reference

**Colors:**
- Blue: #2563EB (light) / #3B82F6 (dark)
- Purple: #7C3AED (light) / #A78BFA (dark)
- Green: #059669 (light) / #10B981 (dark)
- Red: #DC2626 (light) / #EF4444 (dark)
- Yellow: #D97706 (light) / #FBBF24 (dark)

**Badges:**
- New (green): bg-green-50/green-900/20, text-green-700/green-300, border-green-200/green-700
- Returning (blue): bg-blue-50/blue-900/20, text-blue-700/blue-300, border-blue-200/blue-700

---

## 🚀 Implementation Steps

### PART A: DOMAIN SOURCES TAB

---

### Step 1: Create Domain Statistics Component

Navigate to **🧩 Components** page.

**Component: DomainSourceStats**

1. Create frame: **Full width × 140px**
2. Grid: 4 equal columns, gap 24px

**Metrics:**

#### Metric 1: Total Domains
- Label: "Total Domains"
- Value: "156"
- Icon: 🌐

#### Metric 2: New Domains
- Label: "New Domains"
- Value: "42"
- Subtext: "(26.9%)" (green-600/green-400)
- Icon: ✨

#### Metric 3: Returning Domains
- Label: "Returning"
- Value: "114"
- Subtext: "(73.1%)" (blue-600/blue-400)
- Icon: 🔄

#### Metric 4: Avg Links per Domain
- Label: "Avg Links/Domain"
- Value: "1.9"
- Icon: 📊

---

### Step 2: Create Stacked Bar Chart Component

Navigate to **🧩 Components** page.

**Component: DomainSourcesChart**

1. Create Card frame: **Full width × 450px**
2. Card title: "New vs Returning Domains"

**Chart Area:**

Use stacked bar chart design (800×350px):

1. **Bars** (one per month):
   - Width: 50px each
   - Gap: 12px between bars
   - Two segments stacked:

     **Bottom segment (New domains):**
     - Color: blue-600 (light) / blue-500 (dark)

     **Top segment (Returning domains):**
     - Color: purple-600 (light) / purple-500 (dark)

2. **Sample Data** (12 months):
   - Jan: New=3, Returning=5 (Total=8)
   - Feb: New=4, Returning=8 (Total=12)
   - Mar: New=12, Returning=30 (Total=42)
   - Apr: New=8, Returning=20 (Total=28)
   - May: New=9, Returning=23 (Total=32)
   - Jun: New=6, Returning=19 (Total=25)
   - Jul: New=5, Returning=13 (Total=18)
   - Aug: New=6, Returning=16 (Total=22)
   - Sep: New=10, Returning=25 (Total=35)
   - Oct: New=8, Returning=22 (Total=30)
   - Nov: New=7, Returning=19 (Total=26)
   - Dec: New=6, Returning=18 (Total=24)

3. **Axes:**
   - X-axis: Month labels (Jan, Feb, Mar...)
   - Y-axis: Domain count (0, 10, 20, 30, 40)
   - Color: gray-400 (light) / gray-500 (dark)

4. **Grid Lines:**
   - Horizontal only
   - Color: gray-200 (light) / gray-700 (dark)

5. **Legend** (top-right):
   - ■ New domains (blue)
   - ■ Returning domains (purple)

6. **Hover Tooltip** (design state):
   - Background: gray-900 (light) / white (dark)
   - Content:
     - "March 2024"
     - "New: 12 domains"
     - "Returning: 30 domains"
     - "Total: 42 domains"

---

### Step 3: Create Top Referring Domains Table

Navigate to **🧩 Components** page.

**Component: ReferringDomainRow**

1. Create frame: **Full width × 64px**
2. Auto Layout: Horizontal, padding 12px 16px, gap 16px

**Columns:**

1. **Domain**:
   - Width: Flexible (fill)
   - Text: "blog.example.com" (14px, blue-600/blue-400, underlined)

2. **Links**:
   - Width: 80px
   - Text: "8" (14px, semibold, gray-900/gray-100)

3. **First Link**:
   - Width: 120px
   - Text: "2023-05-12" (14px, gray-600/gray-400)

4. **Latest Link**:
   - Width: 120px
   - Text: "2024-03-10" (14px, gray-600/gray-400)

5. **Status Badge**:
   - Width: 100px
   - Component: Badge

   **Badge Variants:**
   - ●RETURN (blue): Multiple links over time
   - ○NEW (green): First link in time period

**Component: TopReferringDomainsCard**

1. Create Card frame
2. Title: "Top Referring Domains"
3. Content:
   - Table header
   - 10+ ReferringDomainRow instances
   - Pagination

---

### Step 4: Assemble Domain Sources Tab

Navigate to **📱 Pages - Light Mode** → **Customer Analysis** page.

1. Add new tab: **"Domain Sources"**
2. Tab content (Auto Layout vertical, gap 24px):

   1. DomainSourceStats component
   2. DomainSourcesChart component
   3. TopReferringDomainsCard component

---

### PART B: COMPARISON TAB

---

### Step 5: Create Period Selection Component

Navigate to **🧩 Components** page.

**Component: PeriodSelector**

1. Create Card frame: **Full width × 180px**
2. Card title: "Compare Two Periods"
3. Auto Layout: Vertical, gap 16px, padding 24px

**Period 1 Row:**
- Frame: Auto Layout horizontal, gap 12px

  - Label: "Period 1:" (14px, semibold)
  - DatePicker: From (instance from FIGMA_ADDON_DATE_FILTER.md)
  - Text: "to"
  - DatePicker: To
  - Badge: "(3 months)" (auto-calculated)

**Period 2 Row:**
- Same structure as Period 1

**Action Row:**
- Frame: Auto Layout horizontal, gap 12px

  - Button: "Compare" (Primary, 140px)
  - Dropdown: "Quick Select" (Secondary, 180px)
    - Options:
      - Month vs Month
      - Quarter vs Quarter
      - Last 3 vs Previous 3
      - Custom

---

### Step 6: Create Comparison Results Component

Navigate to **🧩 Components** page.

**Component: ComparisonResults**

1. Create Card frame: **Full width × Auto**
2. Card title: "Comparison Results"
3. Auto Layout: Vertical, gap 0 (table rows)

**Table Header:**
- Frame: Full width × 48px
- Background: gray-100 (light) / gray-800 (dark)
- Auto Layout: Horizontal, space-between, padding 12px 24px

- Columns:
  - "Metric" (Flexible, 12px, uppercase, semibold)
  - "Period 1 (Jan-Mar)" (140px, 12px, uppercase, semibold)
  - "Period 2 (Apr-Jun)" (140px, 12px, uppercase, semibold)
  - "Change" (160px, 12px, uppercase, semibold)

**Table Rows:**

Each row (Auto Layout horizontal, space-between, padding 16px 24px, height 72px):

#### Row 1: Total Links
- Metric: "Total Links" (14px, gray-700/gray-300)
- Period 1: "72" (20px, bold)
- Period 2: "95" (20px, bold)
- Change: "+23 (+31.9%)" with ↗ (16px, green-600/green-400)

#### Row 2: Unique Domains
- Metric: "Unique Domains"
- Period 1: "34"
- Period 2: "48"
- Change: "+14 (+41.2%)" ↗ (green)

#### Row 3: Target URLs
- Metric: "Target URLs"
- Period 1: "18"
- Period 2: "22"
- Change: "+4 (+22.2%)" ↗ (green)

#### Row 4: New Domains
- Metric: "New Domains"
- Period 1: "12"
- Period 2: "19"
- Change: "+7 (+58.3%)" ↗ (green)

**Change Indicator Variants:**
- ↗ Green: Positive growth (>5%)
- → Blue: Stable (±5%)
- ↘ Yellow: Slight decrease (-5% to -15%)
- ↓ Red: Significant decrease (>-15%)

---

### Step 7: Create Comparison Chart Component

Navigate to **🧩 Components** page.

**Component: ComparisonChart**

1. Create Card frame: **Full width × 400px**
2. Card title: "Visual Comparison"

**Grouped Bar Chart:**

1. Chart area: 800×300px
2. X-axis: Metrics (Links, Domains, URLs, New Domains)
3. Y-axis: Count (0, 20, 40, 60, 80, 100)

For each metric, show **2 bars side-by-side:**
- Period 1 bar: blue-600/blue-500
- Period 2 bar: purple-600/purple-500
- Width: 40px each
- Gap: 8px between bars in same group
- Gap: 48px between groups

**Labels:**
- Value on top of each bar (14px, semibold)
- Metric label on x-axis (14px, gray-600/gray-400)

**Legend:**
- ■ Period 1 (Jan-Mar) - Blue
- ■ Period 2 (Apr-Jun) - Purple

---

### Step 8: Assemble Comparison Tab

Navigate to **📱 Pages - Light Mode** → **Customer Analysis** page.

1. Add new tab: **"Comparison"**
2. Tab content (Auto Layout vertical, gap 24px):

   1. PeriodSelector component
   2. ComparisonResults component
   3. ComparisonChart component

---

### PART C: MANAGE LINKS TAB (CRUD)

---

### Step 9: Create CRUD Toolbar Component

Navigate to **🧩 Components** page.

**Component: ManageLinksToolbar**

1. Create frame: **Full width × 64px**
2. Background: white (light) / gray-800 (dark)
3. Border-bottom: 1px solid gray-200/gray-700
4. Auto Layout: Horizontal, space-between, padding 12px 24px

**Left Section:**
- Auto Layout: Horizontal, gap 12px

  1. **Add Button**:
     - Type: Primary button
     - Text: "+ Add New Link"
     - Width: 140px

  2. **Search Input**:
     - Width: 280px
     - Placeholder: "🔍 Search links..."
     - Icon: Search icon (left side)

**Right Section:**
- Auto Layout: Horizontal, gap 8px

  1. **Filter Dropdown**:
     - Type: Secondary button
     - Text: "Filter ▾"
     - Width: 100px

  2. **Sort Dropdown**:
     - Type: Secondary button
     - Text: "Sort ▾"
     - Width: 100px

  3. **Delete Selected Button**:
     - Type: Danger button (red)
     - Text: "Delete Selected"
     - Width: 140px
     - Disabled state by default (gray)

---

### Step 10: Create Editable Table Row Component

Navigate to **🧩 Components** page.

**Component: EditableLinkRow**

1. Create frame: **Full width × 72px**
2. Auto Layout: Horizontal, padding 12px 16px, gap 12px

**Columns:**

1. **Checkbox**:
   - Width: 40px
   - ☐ Unchecked / ☑ Checked states

2. **ID**:
   - Width: 60px
   - Text: "1" (14px, gray-500/gray-400)

3. **Pub Domain**:
   - Width: 200px
   - Text: "example.com" (14px, gray-900/gray-100)
   - Editable: Double-click to edit

4. **Target URL**:
   - Width: 250px
   - Text: "site.com/about" (14px, blue-600/blue-400, underlined)
   - Truncate with ellipsis

5. **Anchor Text**:
   - Width: 200px
   - Text: "learn more" (14px, gray-900/gray-100)
   - Editable

6. **Date**:
   - Width: 120px
   - Text: "2024-03-15" (14px, gray-600/gray-400)
   - Editable with date picker

7. **Actions**:
   - Width: 100px
   - Auto Layout: Horizontal, gap 8px

   - **Edit Icon**: ✏️
     - Size: 20px
     - Color: blue-600/blue-400
     - Clickable circle: 32px

   - **Delete Icon**: 🗑️
     - Size: 20px
     - Color: red-600/red-400
     - Clickable circle: 32px

**Create Variants:**
- Default
- Hover (background: gray-50/gray-800)
- Selected (checkbox checked, background: blue-50/blue-900/10)
- Editing (input fields active)

---

### Step 11: Create Edit Modal Component

Navigate to **🧩 Components** page.

**Component: EditLinkModal**

1. **Backdrop**:
   - Full screen overlay
   - Background: rgba(0, 0, 0, 0.5)
   - Blur: 4px (optional)

2. **Modal Container**:
   - Width: 540px
   - Max-height: 80vh
   - Background: white (light) / gray-800 (dark)
   - Border-radius: 16px
   - Shadow: xl (0 20px 25px rgba(0,0,0,0.15))
   - Position: Center screen
   - Padding: 0

**Modal Header:**
- Frame: Full width × 64px
- Border-bottom: 1px solid gray-200/gray-700
- Auto Layout: Horizontal, space-between, padding 20px 24px

  - Title: "Edit Link" (20px, bold, gray-900/gray-100)
  - Close button: ✕
    - Size: 24px
    - Color: gray-500/gray-400
    - Hover: gray-700/gray-200
    - Clickable circle: 32px

**Modal Body:**
- Frame: Full width × Auto
- Padding: 24px
- Auto Layout: Vertical, gap 20px

**Form Fields:**

Each field (Auto Layout vertical, gap 6px):

1. **Publishing Domain**:
   - Label: "Publishing Domain *" (14px, semibold, gray-700/gray-300)
   - Input: Text input component (full width)
   - Placeholder: "example.com"
   - Helper text: "The domain where the link was published" (12px, gray-500/gray-400)

2. **Target URL**:
   - Label: "Target URL *"
   - Input: Text input component (full width)
   - Placeholder: "https://yoursite.com/page"
   - Helper text: "The URL this link points to"

3. **Anchor Text**:
   - Label: "Anchor Text *"
   - Input: Text input component (full width)
   - Placeholder: "Click here"
   - Helper text: "The clickable text of the link"

4. **Published Date**:
   - Label: "Published Date * (YYYY-MM-DD)"
   - Input: Date picker component
   - Default: Today's date
   - Calendar icon on right

**Validation Errors:**
- Show below each field if invalid
- Red text (12px, red-600/red-400)
- Example: "⚠ This field is required"

**Modal Footer:**
- Frame: Full width × 80px
- Border-top: 1px solid gray-200/gray-700
- Auto Layout: Horizontal, justify right, padding 20px 24px, gap 12px

  - **Cancel Button**:
    - Type: Secondary button
    - Text: "Cancel"
    - Width: 100px

  - **Save Button**:
    - Type: Primary button
    - Text: "Save Link"
    - Width: 120px
    - Loading state: "Saving..." with spinner

**Create Modal Variants:**
- Add New Link (title: "Add New Link", empty fields)
- Edit Link (title: "Edit Link", pre-filled fields)

---

### Step 12: Create Bulk Actions Bar Component

Navigate to **🧩 Components** page.

**Component: BulkActionsBar**

1. Create frame: **Full width × 56px**
2. Background: blue-50 (light) / blue-900/20 (dark)
3. Border: 1px solid blue-200 (light) / blue-700 (dark)
4. Border-radius: 8px
5. Auto Layout: Horizontal, space-between, padding 12px 24px

**Left Section:**
- Text: "✓ 3 links selected" (14px, blue-700/blue-300)

**Right Section:**
- Auto Layout: Horizontal, gap 12px

  1. **Bulk Edit Button**:
     - Type: Secondary button
     - Text: "Bulk Edit"
     - Width: 100px

  2. **Export Selected Button**:
     - Type: Secondary button
     - Text: "Export Selected"
     - Width: 140px

  3. **Delete Button**:
     - Type: Danger button
     - Text: "Delete"
     - Width: 80px

---

### Step 13: Create Delete Confirmation Modal

Navigate to **🧩 Components** page.

**Component: DeleteConfirmationModal**

1. Backdrop: Same as EditLinkModal

2. Modal Container:
   - Width: 440px
   - Background: white (light) / gray-800 (dark)
   - Border-radius: 16px
   - Shadow: xl
   - Padding: 32px

**Content:**

1. **Icon**:
   - ⚠️ Warning triangle
   - Size: 48px
   - Color: red-600/red-500
   - Centered

2. **Title**:
   - Text: "Delete 3 Links?" (24px, bold, gray-900/gray-100)
   - Centered
   - Margin-top: 16px

3. **Message**:
   - Text: "This action cannot be undone. Are you sure you want to delete these 3 links?" (16px, gray-600/gray-400)
   - Centered
   - Line-height: 1.5
   - Margin-top: 12px

4. **Buttons** (horizontal, gap 12px, margin-top 32px):
   - **Cancel**: Secondary button, width 180px
   - **Delete Permanently**: Danger button (red), width 180px

---

### Step 14: Assemble Manage Links Tab

Navigate to **📱 Pages - Light Mode** → **Customer Analysis** page.

1. Add new tab: **"Manage Links"**
2. Tab content:

   1. **ManageLinksToolbar** component (full width)

   2. **BulkActionsBar** component (conditional, shown when items selected)

   3. **Table Container**:
      - Card component
      - No title
      - Auto Layout: Vertical, gap 0

      - **Table Header** (sticky):
        - Background: gray-100/gray-800
        - Columns: [☐] ID | Pub Domain | Target URL | Anchor Text | Date | Actions

      - **Table Rows** (20 rows):
        - EditableLinkRow instances
        - Alternating backgrounds for readability (optional)

      - **Pagination** (bottom):
        - "Showing 1-20 of 296"
        - Page buttons: [Previous] [1] [2] [3] ... [15] [Next]

   4. **Modals** (overlay, hidden by default):
      - EditLinkModal (for add/edit actions)
      - DeleteConfirmationModal (for delete confirmations)

---

### Step 15: Dark Mode Integration

Navigate to **🌙 Pages - Dark Mode**.

1. Repeat Steps 4, 8, and 14 for all three tabs
2. Ensure all components use dark mode variants:
   - Charts: Lighter colors, darker grids
   - Tables: gray-800 backgrounds
   - Modals: gray-800 backgrounds
   - Badges: Adjusted opacity for readability

---

### Step 16: Responsive Adjustments

**Domain Sources (Tablet/Mobile):**
- Tablet: 2×2 stats grid, chart full width
- Mobile: Vertical stats, simplified chart (hide legend)

**Comparison (Tablet/Mobile):**
- Tablet: Period selector vertical
- Mobile: Hide chart, show table only

**Manage Links (Tablet/Mobile):**
- Tablet: Hide ID and actions columns, add menu button per row
- Mobile: Card view instead of table (1 link per card)

---

### Step 17: Add Developer Annotations

```
=================================
DOMAIN SOURCES TAB
=================================

API Endpoint:
GET /api/advanced/customers/{id}/domain-sources?from_date=YYYY-MM&to_date=YYYY-MM

Response:
{
  "statistics": {
    "total_domains": 156,
    "new_domains": 42,
    "returning_domains": 114,
    "avg_links_per_domain": 1.9
  },
  "monthly_data": [
    {
      "month": "2024-01",
      "new_domains": 3,
      "returning_domains": 5
    }
  ],
  "top_domains": [
    {
      "domain": "blog.example.com",
      "link_count": 8,
      "first_link_date": "2023-05-12",
      "latest_link_date": "2024-03-10",
      "is_new": false
    }
  ]
}

Chart: Use Recharts BarChart with stackId

=================================
COMPARISON TAB
=================================

API Endpoint:
GET /api/advanced/customers/{id}/comparison
  ?period1_from=2024-01&period1_to=2024-03
  &period2_from=2024-04&period2_to=2024-06

Response:
{
  "period1": {
    "total_links": 72,
    "unique_domains": 34,
    "target_urls": 18,
    "new_domains": 12
  },
  "period2": {
    "total_links": 95,
    "unique_domains": 48,
    "target_urls": 22,
    "new_domains": 19
  },
  "changes": {
    "total_links": { "absolute": 23, "percentage": 31.9 },
    "unique_domains": { "absolute": 14, "percentage": 41.2 }
  }
}

=================================
MANAGE LINKS TAB (CRUD)
=================================

API Endpoints:

1. List Links (with pagination):
   GET /api/links?offset=0&limit=20&search=seo&customer_id=1

2. Get Single Link:
   GET /api/links/{link_id}

3. Create Link:
   POST /api/links
   Body: {
     "customer_id": 1,
     "canonical_root": "example.com",
     "brand": "Example Brand",
     "pub_domain": "publisher.com",
     "target_url": "https://example.com/page",
     "anchor_text": "click here",
     "published_at": "2024-03-15"
   }

4. Update Link:
   PUT /api/links/{link_id}
   Body: { "anchor_text": "new anchor" }  # Partial update

5. Delete Link:
   DELETE /api/links/{link_id}

6. Bulk Delete:
   POST /api/links/bulk-delete
   Body: { "link_ids": [1, 2, 3] }

Validation:
- All fields required except in update (partial)
- Date format: YYYY-MM-DD
- URLs must be valid format

State Management:
- Use React Query for CRUD operations
- Optimistic updates for better UX
- Show loading states during operations
- Toast notifications on success/error

Permissions:
- Add check: Can user create links?
- Edit check: Can user modify this link?
- Delete check: Can user delete links?
```

---

## ✅ Implementation Checklist

**Domain Sources Tab:**
- [ ] Create DomainSourceStats (4 metrics)
- [ ] Create DomainSourcesChart (stacked bars)
- [ ] Create ReferringDomainRow
- [ ] Create TopReferringDomainsCard
- [ ] Assemble Domain Sources tab
- [ ] Test light and dark modes

**Comparison Tab:**
- [ ] Create PeriodSelector
- [ ] Create ComparisonResults table
- [ ] Create ComparisonChart (grouped bars)
- [ ] Add quick select dropdown
- [ ] Assemble Comparison tab
- [ ] Test light and dark modes

**Manage Links Tab:**
- [ ] Create ManageLinksToolbar
- [ ] Create EditableLinkRow
- [ ] Create EditLinkModal (add/edit)
- [ ] Create BulkActionsBar
- [ ] Create DeleteConfirmationModal
- [ ] Create table with 20 rows
- [ ] Add pagination
- [ ] Assemble Manage Links tab
- [ ] Test all CRUD interactions
- [ ] Test light and dark modes

**Integration:**
- [ ] Add all 3 tabs to navigation
- [ ] Test tab switching
- [ ] Create responsive layouts
- [ ] Add prototype interactions

**Documentation:**
- [ ] Add API annotations for all endpoints
- [ ] Document CRUD operations
- [ ] Add validation rules
- [ ] Include state management notes

---

## 🎯 Success Criteria

Your implementation is complete when:

1. ✅ Domain Sources shows new vs returning domain trends
2. ✅ Stacked bar chart displays monthly domain breakdown
3. ✅ Top domains table shows status badges (NEW/RETURN)
4. ✅ Comparison tab allows two period selection
5. ✅ Comparison results show side-by-side metrics with changes
6. ✅ Comparison chart visualizes differences
7. ✅ Manage Links toolbar has add, search, filter, delete
8. ✅ Editable table shows all links with actions
9. ✅ Edit modal allows add/edit link with validation
10. ✅ Delete confirmation prevents accidental deletion
11. ✅ Bulk actions work when multiple items selected
12. ✅ All tabs work in light and dark modes
13. ✅ Responsive layouts work on all screen sizes
14. ✅ Developer annotations are comprehensive

---

## 📊 Visual Reference

```
DOMAIN SOURCES:
┌────────────────────────────────────────────────────────────────┐
│ Total: 156  │  New: 42  │  Returning: 114  │  Avg: 1.9       │
├────────────────────────────────────────────────────────────────┤
│ Domains                                                         │
│ 40 │ ████████ (stacked bars: blue=new, purple=returning)      │
│ 30 │ ████████████                                              │
│ 20 │ ████████████████                                          │
│ 10 │ ████████████████████                                      │
│  0 └──────────────────────────                                 │
│    J  F  M  A  M  J  J  A  S  O  N  D                         │
└────────────────────────────────────────────────────────────────┘

COMPARISON:
┌────────────────────────────────────────────────────────────────┐
│ Period 1: [2024-01] to [2024-03]    (3 months)                │
│ Period 2: [2024-04] to [2024-06]    (3 months)                │
│ [Compare]  [Quick Select ▾]                                   │
├────────────────────────────────────────────────────────────────┤
│ Metric          │ Period 1  │ Period 2  │ Change             │
│ Total Links     │ 72        │ 95        │ +23 (+31.9%) ↗     │
│ Unique Domains  │ 34        │ 48        │ +14 (+41.2%) ↗     │
└────────────────────────────────────────────────────────────────┘

MANAGE LINKS:
┌────────────────────────────────────────────────────────────────┐
│ [+ Add] [🔍 Search...]        [Filter▾] [Sort▾] [Delete]     │
├────────────────────────────────────────────────────────────────┤
│ ☐│ID│ Pub Domain  │ Target URL  │ Anchor    │ Date   │ ✏️ 🗑️│
│ ☐│1 │example.com  │site.com/... │learn more │03-15   │ ✏️ 🗑️│
│ ☐│2 │blog.io      │site.com/... │best guide │03-10   │ ✏️ 🗑️│
└────────────────────────────────────────────────────────────────┘

EDIT MODAL:
┌──────────────────────────────┐
│  Edit Link                ✕  │
├──────────────────────────────┤
│  Publishing Domain *         │
│  [example.com]               │
│                              │
│  Target URL *                │
│  [https://site.com/page]     │
│                              │
│  Anchor Text *               │
│  [learn more]                │
│                              │
│  Date * [2024-03-15] 📅      │
│                              │
│  [Cancel]  [Save Link]       │
└──────────────────────────────┘
```

---

**Version:** 1.0
**Estimated Time:** 30-40 minutes
**Difficulty:** ⭐⭐⭐⭐ Advanced
**Dependencies:** FIGMA_DESIGN_PROMPT.md (Phases 1-15), Optional: FIGMA_ADDON_DATE_FILTER.md
