# LinkDB GUI - Step-by-Step Execution Guide

## 📋 Context
You have now received the complete design specification document (FIGMA_DESIGN_PROMPT.md). This guide will help you execute the design in manageable phases.

## 🎯 Working Method

**IMPORTANT RULES:**
1. ✅ Work on ONE phase at a time
2. ✅ Confirm completion of each phase before moving to next
3. ✅ Use exact measurements and colors from specification
4. ✅ Apply Auto Layout to all container components
5. ✅ Create variants for Light/Dark modes
6. ⏸️ STOP after each phase and say "Phase X complete. Ready for next phase?"

---

## 🚀 Phase 1: Color Styles (Start Here)

**Goal**: Create all color styles for light and dark modes

**Tasks:**
1. Open "🎨 Design Tokens" page
2. In the **Colors - Light Mode** frame:
   - Create color swatches (100×100px squares)
   - Label each color with name and hex code
   - Organize in sections: Primary, Background, Text, Border, Status

3. Create Figma Color Styles (⌘⌥K or right-click):
   ```
   Format: "Light/Category/Name"
   Examples:
   - Light/Primary/Blue-600 (#2563EB)
   - Light/Background/Page (#F3F4F6)
   - Light/Text/Primary (#111827)
   ```

4. Repeat for **Colors - Dark Mode** frame:
   ```
   Format: "Dark/Category/Name"
   Examples:
   - Dark/Primary/Blue-400 (#3B82F6)
   - Dark/Background/Page (#111827)
   - Dark/Text/Primary (#F9FAFB)
   ```

**Colors to create** (refer to FIGMA_DESIGN_PROMPT.md section "Color Palette"):
- Primary Colors (2-3 colors)
- Background Colors (4-5 colors)
- Text Colors (4 colors)
- Border Colors (3 colors)
- Status Colors (8 colors: success, warning, danger, info - each with light/dark)

**Stop here and confirm**: "Phase 1 complete. Ready for next phase?"

---

## 🚀 Phase 2: Typography Styles

**Goal**: Create all text styles

**Tasks:**
1. In **Typography Scale** frame:
   - Create text samples showing each style
   - Format: "The quick brown fox..." in each size

2. Create Figma Text Styles:
   ```
   Format: "Category/Size/Weight"
   Examples:
   - Heading/H1/Bold (30px, Bold, 1.25 line-height)
   - Body/Base/Regular (16px, Regular, 1.5 line-height)
   - Label/Small/Medium (14px, Medium, 1.5 line-height)
   ```

**Text styles to create** (refer to specification):
- Heading/H1 through H4
- Body/Large, Body/Base, Body/Small
- Label/Large, Label/Base, Label/Small
- Each with appropriate color (Light/Text/Primary or Dark/Text/Primary)

**Stop here and confirm**: "Phase 2 complete. Ready for next phase?"

---

## 🚀 Phase 3: Core Components - Part 1 (Card, Button, Badge)

**Goal**: Create the most used components with variants

**Tasks:**

### 3.1 Card Component
1. Create frame: 400 × 300px
2. Apply Auto Layout (⇧⌥A):
   - Direction: Vertical
   - Padding: 24px
   - Gap: 16px
3. Add background fill: Light/Background/Card
4. Add border-radius: 8px
5. Add shadow: (refer to specification)
6. Create component: ⌘⌥K

**Create Variants**:
- Property 1: Theme (Light, Dark)
- Property 2: Title (With Title, Without Title)

For "With Title" variant:
- Add text layer: Text/Heading/Medium
- Content: "Card Title"
- Apply Title text style

For Dark variant:
- Change background to: Dark/Background/Card
- Update text color to: Dark/Text/Primary

### 3.2 Button Component
1. Create frame: Auto × 40px
2. Apply Auto Layout:
   - Direction: Horizontal
   - Padding: 16px horizontal, 8px vertical
   - Gap: 8px
3. Add text: "Button"
4. Border-radius: 8px
5. Create component

**Create Variants**:
- Property 1: Theme (Light, Dark)
- Property 2: Type (Primary, Secondary, Danger)
- Property 3: State (Default, Hover, Disabled)

Apply colors from specification for each combination.

### 3.3 Badge Component
1. Create frame: Auto × 24px
2. Apply Auto Layout:
   - Padding: 10px horizontal, 2px vertical
   - Border-radius: 9999px (full)
3. Add text: "Badge" (12px, Medium)
4. Create component

**Create Variants**:
- Property 1: Theme (Light, Dark)
- Property 2: Type (Default, Success, Warning, Danger, Info)

Apply colors from specification.

**Stop here and confirm**: "Phase 3 complete. Ready for next phase?"

---

## 🚀 Phase 4: Core Components - Part 2 (Input, Table Elements)

**Goal**: Create form and table components

### 4.1 Input Component
1. Create frame: 320 × 40px
2. Apply Auto Layout:
   - Padding: 16px horizontal, 8px vertical
3. Border: 1px solid Light/Border/Input
4. Border-radius: 8px
5. Add placeholder text: "Placeholder text"
6. Create component

**Create Variants**:
- Theme (Light, Dark)
- State (Default, Focus, Disabled)

### 4.2 Table Components
Create as separate components:
1. **Table Header Cell** (component)
2. **Table Cell** (component)
3. **Table Row** (component using header/cell components)

Apply styling from specification.

**Stop here and confirm**: "Phase 4 complete. Ready for next phase?"

---

## 🚀 Phase 5: Layout Components (Header, Sidebar)

**Goal**: Create main layout structure

### 5.1 Header Component
1. Create frame: 1184 × 64px (full width minus sidebar)
2. Apply Auto Layout:
   - Direction: Horizontal
   - Padding: 16px
   - Justify: Space between
3. Add title text: "Analytics Dashboard"
4. Add Theme Toggle button (use Button component instance)
5. Apply background: Light/Background/Card
6. Border-bottom: 1px solid Light/Border/Default

**Create Variants**:
- Theme (Light, Dark)

### 5.2 Sidebar Component
1. Create frame: 256 × 1024px
2. Apply Auto Layout:
   - Direction: Vertical
   - Padding: 16px
3. Add logo section (80px height)
4. Add navigation items (use reference from specification)

**Create navigation item component**:
- Default state
- Active state
- Hover state
- Light/Dark variants

**Stop here and confirm**: "Phase 5 complete. Ready for next phase?"

---

## 🚀 Phase 6: Specialized Components (Health Gauge, Charts, AI Components)

**Goal**: Create unique components

### 6.1 Health Gauge
- Create circular progress indicator (SVG or plugin)
- Sizes: 80px, 150px
- Color coding based on score
- Center text showing score

### 6.2 Chart Placeholders
- Create frames with annotations
- Label: "Recharts - Pie Chart" etc.
- Add notes with specifications

### 6.3 AI Components
- **AI Chat Message Bubble** (User/AI variants)
- **Insights Panel** (with gradient background)
- **Recommendations Card**

Apply styling from specification.

**Stop here and confirm**: "Phase 6 complete. Ready for next phase?"

---

## 🚀 Phase 7: Page - Dashboard (Light Mode)

**Goal**: Compose first page using components

**Tasks:**
1. Go to "📱 Pages - Light Mode" page
2. Open "Dashboard" frame (1440 × 1024px)
3. Place Sidebar component on left
4. Place Header component on top-right
5. Add main content area:
   - Page title: "Dashboard" (H1 style)
   - KPI Cards row (3 columns, 24px gap)
   - Top Performers table card

Use instances of components created earlier.
Apply exact spacing from specification (24px margins, etc.)

**Stop here and confirm**: "Phase 7 complete. Ready for next phase?"

---

## 🚀 Phase 8: Page - Customer List (Light Mode)

**Goal**: Create customer list page

**Structure:**
1. Page title
2. Search card (with Input component)
3. Table card (using Table components)

Follow layout specification exactly.

**Stop here and confirm**: "Phase 8 complete. Ready for next phase?"

---

## 🚀 Phase 9: Page - Customer Analysis (Light Mode)

**Goal**: Create detailed analysis page with tabs

**Structure:**
1. Header (customer name + brand)
2. Executive summary card
3. Key metrics (3 cards)
4. Tab navigation
5. Tab content (create all 6 tabs)

This is the most complex page - take your time.

**Stop here and confirm**: "Phase 9 complete. Ready for next phase?"

---

## 🚀 Phase 10: Remaining Pages (Light Mode)

**Goal**: Complete all pages

Create:
1. Link Explorer
2. Competitive Benchmarking
3. AI Chat
4. Settings

Each page follows specification layout.

**Stop here and confirm**: "Phase 10 complete. Ready for next phase?"

---

## 🚀 Phase 11: Dark Mode Pages

**Goal**: Create all dark mode versions

**Tasks:**
1. Go to "🌙 Pages - Dark Mode"
2. For each page:
   - Duplicate from light mode
   - Swap all component instances to Dark theme variants
   - Verify all colors are correct
   - Check hover states

**Stop here and confirm**: "Phase 11 complete. Ready for next phase?"

---

## 🚀 Phase 12: Responsive Layouts

**Goal**: Create mobile and tablet versions

For each page, create additional frames:
- Mobile: 375 × 812px
- Tablet: 768 × 1024px

Adjust layouts according to responsive specifications:
- Mobile: 1 column grids, hidden sidebar
- Tablet: 2 column grids, collapsible sidebar

**Stop here and confirm**: "Phase 12 complete. Ready for next phase?"

---

## 🚀 Phase 13: Prototyping

**Goal**: Add interactions

**Tasks:**
1. **Theme Toggle**: Link light/dark versions
   - Select theme toggle button
   - Add interaction: Navigate to → Dark mode page
   - Animation: Dissolve, 200ms

2. **Navigation**: Link sidebar items to pages
   - Select nav item
   - Add interaction: Navigate to → Page
   - Animation: Smart Animate

3. **Tabs**: Link tab buttons to content
   - On Customer Analysis page
   - Link each tab to respective content frame

4. **Table Rows**: Link to detail pages
   - Customer list → Customer Analysis
   - Add hover state

**Stop here and confirm**: "Phase 13 complete. Ready for next phase?"

---

## 🚀 Phase 14: Developer Annotations

**Goal**: Add specifications for developers

**Tasks:**
1. Use Annotation tool or sticky notes
2. Add notes to components:
   - Tailwind CSS classes (e.g., "bg-gray-100 dark:bg-gray-900")
   - Spacing measurements (e.g., "gap-6 = 24px")
   - Component props (e.g., "title: optional string")

3. Create "📐 Specs & Annotations" page
4. Add key measurements:
   - Sidebar width: 256px
   - Header height: 64px
   - Content padding: 32px
   - Card padding: 24px
   - Grid gaps: 24px
   - Border radius: 8px

**Stop here and confirm**: "Phase 14 complete. Ready for next phase?"

---

## 🚀 Phase 15: Final Polish & Export

**Goal**: Finalize and prepare deliverables

**Tasks:**
1. **Review Checklist**:
   - [ ] All colors defined as styles
   - [ ] All text styles created
   - [ ] All components have variants
   - [ ] All 7 pages designed (light + dark)
   - [ ] Responsive layouts created
   - [ ] Prototype flows working
   - [ ] Developer annotations added
   - [ ] Naming is consistent

2. **Create Cover Page**:
   - Project title: "LinkDB GUI Design System"
   - Version: 1.0
   - Date
   - Overview of pages
   - Color palette preview
   - Typography preview

3. **Export Preparations**:
   - Organize layers with clear naming
   - Group related elements
   - Add descriptions to components
   - Create component documentation

**Stop here and confirm**: "Phase 15 complete. Base design ready for handoff!"

---

## 🚀 Phase 16: Date Range Filter Component (Advanced Features)

**Goal**: Add global date range filtering to Customer Analysis page

**Tasks:**

1. **Create DateRangeFilter Component**:
   - Frame: Auto width × 80px height
   - Apply Auto Layout: Horizontal, padding 24px, gap 16px
   - Background: white (light) / gray-800 (dark)
   - Border-radius: 8px
   - Shadow: default card shadow

2. **Add Date Picker Inputs**:
   ```
   Left side:
   - Label: "From" (12px, semibold, gray-700/gray-300)
   - Input: 150px wide, standard input styling
   - Placeholder: "YYYY-MM" or "2024-01"
   - Dropdown icon (▾)

   Arrow icon: → (20px, gray-400, margin 0 8px)

   Right side:
   - Label: "To" (12px, semibold)
   - Input: 150px wide, same styling
   - Placeholder: "YYYY-MM" or "2024-12"
   - Dropdown icon (▾)
   ```

3. **Add Action Buttons**:
   - "Apply Filter" button (Primary)
   - "Clear" button (Secondary)
   - Gap: 8px between buttons

4. **Add Active Filter Indicator**:
   ```
   When filter is active:
   - Background: blue-50 (light) / blue-900/20 (dark)
   - Border: 1px solid blue-200/blue-800
   - Padding: 8px 12px
   - Border-radius: 6px
   - Text: "📅 Jan 2024 - Dec 2024" (14px, blue-700/blue-400)
   - X icon to clear (16px, clickable)
   - Align to right (margin-left: auto)
   ```

5. **Create Component Variants**:
   - Theme: Light, Dark
   - State: Empty, Active (with date range shown)

6. **Place on Customer Analysis Page**:
   - Position: After "Key Metrics" cards, before "Tabs"
   - Full width
   - Margin-bottom: 24px

**Stop here and confirm**: "Phase 16 complete. Ready for next phase?"

---

## 🚀 Phase 17: Enhanced Anchor Analysis Tab

**Goal**: Add 4 sub-views to existing Anchor Analysis tab

**Tasks:**

1. **Create Toolbar Component** (at top of Anchor Analysis content):
   ```
   Layout: Horizontal, space-between

   Left side - Tab Pills:
   - [Distribution] [Frequency] [Word Cloud] [Search]
   - Inactive: transparent bg, gray-600/gray-400 text
   - Active: blue-50/blue-900/20 bg, blue-600/blue-400 text
   - Border-bottom: 2px (transparent/active color)
   - Padding: 8px 16px each
   - Gap: 8px between pills

   Right side:
   - Export button (CSV icon)
   - Settings icon
   ```

2. **Create Frequency View** (New):
   ```
   Card: "Anchor Text Frequency"

   Statistics Panel (top):
   - Background: gray-50/gray-900
   - Padding: 16px
   - Display: flex, space-evenly
   - Stats: Total Links | Unique Anchors | Top Usage % | Diversity Score

   Table:
   Columns: Rank | Anchor Text | Count | Percentage | Visual Bar
   - Rank: gray-500, 14px
   - Anchor Text: gray-900/gray-100, 14px, medium
   - Count: gray-700/gray-300, 14px
   - Percentage: gray-700/gray-300, 14px
   - Visual Bar: Blue bar proportional to percentage
   - Rows: Hover bg gray-50/gray-700/50
   - Sortable headers (add ↕ icon)
   ```

3. **Create Word Cloud View** (New):
   ```
   Card: "Word Frequency in Anchors"

   Controls (top):
   - Min word length: Dropdown [3▾]
   - Exclude common words: Checkbox [✓]
   - Show top: Dropdown [100▾] words
   - Inline layout with 16px gap

   Table:
   Columns: Word | Frequency | Used in X anchors | Visual Bar
   - Same styling as Frequency table
   - Click word to highlight in context
   ```

4. **Create Search View** (New):
   ```
   Card: "Search Anchor Texts"

   Search Bar:
   - Input: Full width, "🔍 Search for word or phrase..."
   - Checkbox: "☐ Case sensitive" below input
   - Search button (Primary)

   Results Table (after search):
   - Header: "Found X links containing 'search term'"
   - Columns: Anchor Text | Pub Domain | Date
   - Export button: "Export Results (CSV)"
   - Empty state: 🔍 icon + "Enter search term above"
   ```

5. **Wire Tab Switching**:
   - Link each pill to show/hide respective view
   - Default: Distribution (existing pie chart)
   - Add smooth transitions

**Stop here and confirm**: "Phase 17 complete. Ready for next phase?"

---

## 🚀 Phase 18: New Analysis Tabs - Part 1

**Goal**: Create Target URLs and Link Velocity tabs

**Tasks:**

1. **Add New Tabs to Navigation**:
   ```
   Update tab list to include:
   1. Overview
   2. Anchor Analysis
   3. Temporal Patterns
   4. Domain Quality
   5. Target URLs ← NEW
   6. Link Velocity ← NEW
   7. 🤖 AI Assistant

   (We'll add more in Phase 19)
   ```

2. **Create Target URLs Tab Content**:
   ```
   Card 1: "Target URL Statistics"
   Grid (4 columns, 24px gap):
   - Total URLs: [147] (2xl, bold)
   - Homepage Links: [52 (35.4%)] (2xl, bold)
   - Deep Links: [95 (64.6%)] (2xl, bold)
   - Diversity: [78/100] (2xl, bold)
   Labels: 14px, gray-600/gray-400

   Card 2: "Deep Linking Distribution"
   - Pie/Donut chart (400×300px)
   - Segments:
     * Homepage: 35.4% (blue-600)
     * Category pages: 28.3% (purple-600)
     * Blog posts: 22.1% (green-600)
     * Product pages: 14.2% (yellow-500)
   - Legend on right side

   Card 3: "Top Target URLs"
   Table:
   - Columns: Rank | Target URL | Links | Type | Visual Bar
   - Type badges: Homepage (blue), Blog Post (purple), Category (green), Page (gray)
   - Visual bars: Proportional to link count
   - Rows: 10-20 URLs
   ```

3. **Create Link Velocity Tab Content**:
   ```
   Card 1: "Velocity Metrics"
   Grid (4 columns):
   - Avg/Month: [24.5 links] (2xl, bold)
   - Trend: [↗ Accelerating] (2xl, bold, green if ↗, yellow if ↘)
   - Peak Month: [42 (Mar'24)] (2xl, bold)
   - Low Month: [8 (Jan'24)] (2xl, bold)

   Card 2: "Monthly Velocity Chart"
   - Line chart (600×400px)
   - Recharts LineChart specification:
     * Blue line (#3B82F6 light / #60A5FA dark)
     * Dots on each month
     * Grid lines (horizontal)
     * X-axis: Months (Jan, Feb, Mar...)
     * Y-axis: Link count
     * Tooltip on hover
     * Trend line (dotted, gray)

   Card 3: "Velocity Insights"
   List of insights with icons:
   - ✓ (green): Positive insights
   - ⚠ (yellow): Attention points
   - ℹ (blue): Information
   - ✗ (red): Warnings
   Examples:
   "✓ Steady growth over last 6 months (+15% average)"
   "⚠ Peak activity in March (42 links) - campaign launch?"
   ```

4. **Add Chart Placeholder Annotations**:
   - Label: "Recharts LineChart"
   - Note: "See API_ENDPOINTS_REFERENCE.md for data format"
   - Note: "GET /api/advanced/customers/{id}/link-velocity"

**Stop here and confirm**: "Phase 18 complete. Ready for next phase?"

---

## 🚀 Phase 19: New Analysis Tabs - Part 2

**Goal**: Create Domain Sources and Comparison tabs

**Tasks:**

1. **Add Remaining Tabs to Navigation**:
   ```
   Complete tab list:
   1. Overview
   2. Anchor Analysis
   3. Temporal Patterns
   4. Domain Quality
   5. Target URLs
   6. Link Velocity
   7. Domain Sources ← NEW
   8. Comparison ← NEW
   9. 🤖 AI Assistant

   (Manage Links tab comes in Phase 20)
   ```

2. **Create Domain Sources Tab Content**:
   ```
   Card 1: "Domain Statistics"
   Grid (4 columns):
   - Total Domains: [156] (2xl, bold)
   - New Domains: [42 (26.9%)] (2xl, bold, green)
   - Returning: [114 (73.1%)] (2xl, bold, blue)
   - Avg Links/Domain: [1.9] (2xl, bold)

   Card 2: "New vs Returning Domains"
   - Stacked bar chart (600×400px)
   - Monthly view
   - Blue bars: New domains (#3B82F6)
   - Purple bars: Returning domains (#8B5CF6)
   - Legend below chart
   - Recharts BarChart with stacked property

   Card 3: "Top Referring Domains"
   Table:
   - Columns: Domain | Links | First Link | Latest Link | Status
   - Status badges:
     * ●RETURN (blue) = multiple links
     * ○NEW (green) = single link
   - Sortable by all columns
   - 20-30 rows
   ```

3. **Create Comparison Tab Content**:
   ```
   Card 1: "Period Selection"
   Layout:
   - Title: "Compare Two Periods" (20px, semibold)
   - Period 1: [2024-01▾] to [2024-03▾] (3 months)
   - Period 2: [2024-04▾] to [2024-06▾] (3 months)
   - Buttons: [Compare] [Quick Select▾]
   - Quick Select dropdown:
     * Month vs Month
     * Quarter vs Quarter
     * Last 3m vs Previous 3m
     * Custom

   Card 2: "Comparison Results"
   Side-by-side table:
   ┌─────────────────┬──────────┬──────────┬──────────────┐
   │                 │ Period 1 │ Period 2 │ Change       │
   ├─────────────────┼──────────┼──────────┼──────────────┤
   │ Total Links     │ 72       │ 95       │ +23 (+31.9%)↗│
   │ Unique Domains  │ 34       │ 48       │ +14 (+41.2%)↗│
   │ Target URLs     │ 18       │ 22       │ +4  (+22.2%)↗│
   │ New Domains     │ 12       │ 19       │ +7  (+58.3%)↗│
   └─────────────────┴──────────┴──────────┴──────────────┘

   Change indicators:
   - ↗ green: Positive growth
   - → blue: Stable
   - ↘ yellow: Slight decrease
   - ↓ red: Significant decrease

   Card 3: "Visual Comparison"
   - Bar chart (500×400px)
   - Side-by-side bars for each metric
   - Blue bars: Period 1 (#3B82F6)
   - Purple bars: Period 2 (#8B5CF6)
   - Legend below
   ```

**Stop here and confirm**: "Phase 19 complete. Ready for next phase?"

---

## 🚀 Phase 20: Manage Links Tab (CRUD Interface)

**Goal**: Create full CRUD interface for link management

**Tasks:**

1. **Add Final Tab to Navigation**:
   ```
   Complete tab list (10 tabs total):
   1. Overview
   2. Anchor Analysis
   3. Temporal Patterns
   4. Domain Quality
   5. Target URLs
   6. Link Velocity
   7. Domain Sources
   8. Comparison
   9. Manage Links ← NEW
   10. 🤖 AI Assistant
   ```

2. **Create Manage Links Toolbar**:
   ```
   Layout: Horizontal, space-between

   Left side:
   - [+ Add New Link] button (Primary)
   - [🔍 Search] input (300px)
   - [Filter▾] dropdown
   - [Sort▾] dropdown

   Right side:
   - [Delete Selected] button (Danger, disabled if none selected)
   ```

3. **Create Editable Links Table**:
   ```
   Columns: ☐ | ID | Pub Domain | Target URL | Anchor Text | Date | Actions

   Header styling:
   - Checkbox: Select all
   - Column headers: 14px, semibold, gray-700/gray-300
   - Sortable: Add ↕ icon to headers

   Row styling:
   - Checkbox: Individual selection
   - ID: gray-500, 14px
   - Text: gray-900/gray-100, 14px
   - Hover: gray-50/gray-700/50 background
   - Selected: blue-50/blue-900/20 background
   - Border-left: 3px blue-600 when selected

   Actions column:
   - ✏️ Edit icon (clickable, blue on hover)
   - 🗑️ Delete icon (clickable, red on hover)
   - Gap: 8px between icons
   ```

4. **Create Add/Edit Modal**:
   ```
   Modal specs:
   - Width: 500px
   - Max-height: 80vh
   - Background: white/gray-800
   - Border-radius: 12px
   - Shadow: xl
   - Backdrop: rgba(0,0,0,0.5)

   Header:
   - Title: "Add New Link" or "Edit Link"
   - Close X button (top-right)

   Form fields:
   - Publishing Domain * (required)
   - Target URL * (required)
   - Anchor Text * (required)
   - Published Date * (YYYY-MM-DD) with calendar picker 📅
   - All use standard input styling
   - Labels: 14px, semibold
   - Spacing: 16px between fields

   Footer:
   - [Cancel] button (Secondary)
   - [Save Link] button (Primary)
   - Right-aligned, 8px gap

   Validation:
   - Red border on error
   - Error text below field (12px, red-600)
   - Disable Save if invalid
   ```

5. **Create Bulk Actions UI**:
   ```
   When items selected:
   - Show banner at top of table:
     "✓ 3 links selected"
   - Buttons:
     [Bulk Edit] [Export Selected] [Delete]
   - Background: blue-50/blue-900/20
   - Padding: 12px 16px
   - Border-radius: 8px
   ```

6. **Create Delete Confirmation Dialog**:
   ```
   Modal specs:
   - Width: 400px
   - Title: "⚠️ Delete X Link(s)?"
   - Message: "This action cannot be undone..."
   - Buttons:
     [Cancel] (Secondary)
     [Delete Permanently] (Danger)
   ```

7. **Add Success/Error Toasts**:
   ```
   Toast component:
   - Position: Top-right
   - Width: 350px
   - Success: Green background, checkmark icon
   - Error: Red background, X icon
   - Auto-dismiss after 3 seconds
   - Messages:
     * "Link created successfully"
     * "Link updated successfully"
     * "3 links deleted"
     * "Error: [message]"
   ```

**Stop here and confirm**: "Phase 20 complete. All advanced features added!"

---

## 🎯 After Completion

Once all phases are done:

1. **Share Prototype**: Get prototype link (Share → Copy link)
2. **Export Components**: Select components → Export
3. **Create Spec PDF**: Export "📐 Specs & Annotations" page as PDF
4. **Developer Handoff**: Use Figma's Dev Mode or create handoff document

---

## 💡 Tips While Working

- **Save frequently**: Figma autosaves, but create version checkpoints after each phase
- **Use consistent naming**: Follow naming conventions in specification
- **Apply Auto Layout**: Makes components responsive and easier to adjust
- **Create variants wisely**: Organize properties logically (Theme → Type → State)
- **Test dark mode**: Switch between light/dark to ensure readability
- **Check spacing**: Use 8px grid (4, 8, 16, 24, 32, 48)
- **Verify colors**: All colors should come from styles, not arbitrary values
- **Document decisions**: Add notes for any deviations from specification

---

## ⚡ Quick Reference

**Keyboard Shortcuts:**
- ⌘⌥K: Create component
- ⇧⌥A: Add Auto Layout
- ⌘D: Duplicate
- ⌘/: Search for anything
- ⌥: Show spacing while hovering

**Common Frame Sizes:**
- Desktop page: 1440 × 1024px
- Tablet: 768 × 1024px
- Mobile: 375 × 812px
- Component: Auto or specific from spec

**Default Spacing:**
- Component padding: 24px (p-6)
- Section gaps: 24px (gap-6)
- Grid gaps: 24px (gap-6)
- Card padding: 24px (p-6)
- Button padding: 16px h, 8px v (px-4 py-2)

---

## 🚦 Current Phase Tracker

**As you complete each phase, update this:**

**Base Design System (Required):**
- [ ] Phase 1: Color Styles
- [ ] Phase 2: Typography Styles
- [ ] Phase 3: Core Components Part 1
- [ ] Phase 4: Core Components Part 2
- [ ] Phase 5: Layout Components
- [ ] Phase 6: Specialized Components
- [ ] Phase 7: Dashboard Page
- [ ] Phase 8: Customer List Page
- [ ] Phase 9: Customer Analysis Page
- [ ] Phase 10: Remaining Pages
- [ ] Phase 11: Dark Mode Pages
- [ ] Phase 12: Responsive Layouts
- [ ] Phase 13: Prototyping
- [ ] Phase 14: Developer Annotations
- [ ] Phase 15: Final Polish & Export

**Advanced Features (Optional - Use Addon Prompts):**
- [ ] Phase 16: Date Range Filter (or use FIGMA_ADDON_DATE_FILTER.md)
- [ ] Phase 17: Enhanced Anchor Analysis (or use FIGMA_ADDON_ENHANCED_ANCHOR.md)
- [ ] Phase 18: New Analysis Tabs Part 1 (or use FIGMA_ADDON_ANALYSIS_TABS_1.md)
- [ ] Phase 19: New Analysis Tabs Part 2 (or use FIGMA_ADDON_ANALYSIS_TABS_2.md)
- [ ] Phase 20: Manage Links Tab (included in FIGMA_ADDON_ANALYSIS_TABS_2.md)

---

## 🎬 Ready to Start?

**Begin with Phase 1: Color Styles**

Remember:
1. Work on ONE phase at a time
2. Follow specifications exactly
3. Confirm completion before moving forward
4. Take breaks between phases if needed

**Let's create an amazing design system! 🚀**
