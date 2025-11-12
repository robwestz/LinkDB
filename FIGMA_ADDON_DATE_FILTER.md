# 🗓️ LinkDB Addon: Date Range Filter

## 📋 Overview

This addon adds **global date range filtering** to the LinkDB Customer Analysis page. Users can filter all analysis data by specific time periods (month/year format).

**⏱️ Estimated Time:** 20-30 minutes
**📦 Prerequisites:** Base design from `FIGMA_DESIGN_PROMPT.md` (Phases 1-15 completed)
**🎯 Outcome:** Date range filter component integrated into Customer Analysis page

---

## 🎨 Design System Reference

Use the existing design system from `FIGMA_DESIGN_PROMPT.md`:

**Colors (Light Mode):**
- Primary Blue: #2563EB (blue-600)
- Background: #F3F4F6 (gray-100)
- Card: #FFFFFF (white)
- Text: #111827 (gray-900)
- Border: #E5E7EB (gray-200)

**Colors (Dark Mode):**
- Primary Blue: #3B82F6 (blue-500)
- Background: #111827 (gray-900)
- Card: #1F2937 (gray-800)
- Text: #F9FAFB (gray-50)
- Border: #374151 (gray-700)

**Typography:**
- Font family: Inter
- Headings: 600 weight
- Body: 400 weight
- Small text: 12px
- Body text: 14px
- Headings: 16-24px

**Spacing:** 8px base unit (8, 16, 24, 32, 48, 64px)

---

## 🚀 Implementation Steps

### Step 1: Create DatePicker Component

Navigate to the **🧩 Components** page.

#### 1.1 Create Month/Year Picker Input

**Component: DatePicker**

1. Create a frame: **220px width × 80px height**
2. Apply **Auto Layout**:
   - Direction: Vertical
   - Padding: 0
   - Gap: 4px
   - Alignment: Left

3. Add **Label**:
   - Text: "Month/Year"
   - Font: Inter, 12px, Semibold (600)
   - Color: gray-700 (light) / gray-300 (dark)

4. Add **Input Field**:
   - Frame: 220px × 40px
   - Background: white (light) / gray-800 (dark)
   - Border: 1px solid gray-300 (light) / gray-600 (dark)
   - Border-radius: 8px
   - Padding: 8px 12px

5. Inside Input, add:
   - **Text**: "2024-03" (placeholder)
     - Font: Inter, 14px, Regular
     - Color: gray-900 (light) / gray-100 (dark)

   - **Chevron Icon**: ▾
     - Position: Absolute, right 12px
     - Size: 16px
     - Color: gray-500 (light) / gray-400 (dark)

#### 1.2 Create Dropdown Picker

**Component: DatePickerDropdown**

1. Create a frame: **280px width × 240px height**
2. Background: white (light) / gray-800 (dark)
3. Border: 1px solid gray-200 (light) / gray-700 (dark)
4. Border-radius: 12px
5. Shadow: 0 10px 25px rgba(0,0,0,0.15)

6. **Header (Year Selector):**
   - Frame: Full width × 48px
   - Auto Layout: Horizontal, space-between
   - Padding: 12px 16px
   - Border-bottom: 1px solid gray-200 (light) / gray-700 (dark)

   - **Left Arrow**: ◄
     - Size: 20px
     - Color: gray-600 (light) / gray-400 (dark)
     - Clickable area: 32px circle

   - **Year Text**: "2024"
     - Font: Inter, 16px, Semibold
     - Color: gray-900 (light) / gray-100 (dark)

   - **Right Arrow**: ►
     - Size: 20px
     - Color: gray-600 (light) / gray-400 (dark)
     - Clickable area: 32px circle

7. **Month Grid:**
   - Frame: Full width × 192px
   - Padding: 16px
   - Grid: 3 columns × 4 rows
   - Gap: 8px

   - **Each Month Cell**:
     - Size: 72px × 36px
     - Border-radius: 6px
     - Font: Inter, 14px, Medium
     - Text alignment: Center

     **States:**
     - Default:
       - Background: transparent
       - Text: gray-700 (light) / gray-300 (dark)

     - Hover:
       - Background: gray-100 (light) / gray-700 (dark)
       - Text: gray-900 (light) / gray-100 (dark)

     - Selected:
       - Background: blue-600 (light) / blue-500 (dark)
       - Text: white

#### 1.3 Create Component Variants

Create **4 variants** of DatePicker:
1. Light / Empty
2. Light / Selected
3. Dark / Empty
4. Dark / Selected

**Properties:**
- Mode: Light | Dark
- State: Empty | Selected

---

### Step 2: Create DateRangeFilter Component

Navigate to **🧩 Components** page.

#### 2.1 Main Filter Container

**Component: DateRangeFilter**

1. Create a frame: **Full width (1200px) × 100px**
2. Background: white (light) / gray-800 (dark)
3. Border: 1px solid gray-200 (light) / gray-700 (dark)
4. Border-radius: 12px
5. Shadow: sm (0 1px 2px rgba(0,0,0,0.05))

6. Apply **Auto Layout**:
   - Direction: Horizontal
   - Padding: 24px
   - Gap: 16px
   - Alignment: Center

#### 2.2 Add Components to Container

**Left Section:**

1. **Section Label**:
   - Text: "Filter by Date Range"
   - Font: Inter, 14px, Semibold
   - Color: gray-900 (light) / gray-100 (dark)

2. **"From" DatePicker**:
   - Instance of DatePicker component
   - Label: "From"

3. **Arrow Icon**:
   - Text: "→"
   - Font-size: 20px
   - Color: gray-400 (light) / gray-500 (dark)
   - Margin: 0 8px

4. **"To" DatePicker**:
   - Instance of DatePicker component
   - Label: "To"

**Action Buttons:**

5. **Apply Button**:
   - Instance of Button component (Primary variant)
   - Text: "Apply Filter"
   - Width: 120px
   - Margin-left: 16px

6. **Clear Button**:
   - Instance of Button component (Secondary variant)
   - Text: "Clear"
   - Width: 80px
   - Margin-left: 8px

**Right Section (Auto margin-left):**

7. **Active Filter Indicator** (when filter is applied):
   - Frame: Auto width × 40px
   - Background: blue-50 (light) / rgba(59, 130, 246, 0.2) (dark)
   - Border: 1px solid blue-200 (light) / blue-800 (dark)
   - Border-radius: 8px
   - Padding: 8px 12px
   - Auto Layout: Horizontal, gap 8px

   - **Calendar Icon**: 📅
     - Font-size: 16px

   - **Text**: "Jan 2024 - Dec 2024"
     - Font: Inter, 14px, Medium
     - Color: blue-700 (light) / blue-400 (dark)

   - **Close Icon**: ✕
     - Font-size: 16px
     - Color: blue-600 (light) / blue-400 (dark)
     - Clickable area: 24px circle
     - Hover: background blue-100 (light) / blue-900/50 (dark)

#### 2.3 Create Component Variants

Create **4 variants** of DateRangeFilter:
1. Light / Inactive (no filter applied)
2. Light / Active (filter applied, shows indicator)
3. Dark / Inactive
4. Dark / Active

**Properties:**
- Mode: Light | Dark
- State: Inactive | Active

---

### Step 3: Integrate into Customer Analysis Page

Navigate to **📱 Pages - Light Mode** → **Customer Analysis** page.

#### 3.1 Add Filter to Page

1. **Position**: Between "Key Metrics Cards" and "Tabs Section"
2. **Margin-top**: 32px from Key Metrics
3. **Margin-bottom**: 24px from Tabs

4. **Instance**: Drag DateRangeFilter component
   - Width: Full width (respects container padding)
   - Variant: Light / Inactive (default state)

#### 3.2 Add Second Instance for Active State

1. Create a **second version** of the Customer Analysis page
2. Name it: "Customer Analysis - Filtered"
3. Use DateRangeFilter variant: Light / Active
4. This shows the "after filter applied" state

---

### Step 4: Dark Mode Integration

Navigate to **🌙 Pages - Dark Mode** → **Customer Analysis** page.

1. Add DateRangeFilter component
2. Variant: Dark / Inactive
3. Position: Same as light mode (between metrics and tabs)

4. Create second page: "Customer Analysis - Filtered"
5. Use DateRangeFilter variant: Dark / Active

---

### Step 5: Responsive Adjustments

#### 5.1 Tablet Layout (768px)

Navigate to **Customer Analysis** page → Tablet frame.

**Modifications:**
1. DateRangeFilter:
   - Stack vertically on smaller screens
   - Change Auto Layout direction to: Vertical
   - Align-items: Stretch
   - Gap: 16px

2. Date pickers and buttons:
   - Full width on tablet
   - Maintain horizontal layout for From → To pickers

3. Active filter indicator:
   - Move to new row below buttons
   - Full width

#### 5.2 Mobile Layout (375px)

Navigate to **Customer Analysis** page → Mobile frame.

**Modifications:**
1. DateRangeFilter:
   - Vertical stack
   - Padding: 16px

2. From/To pickers:
   - Vertical stack (no arrow between)
   - Full width (335px)
   - Gap: 12px

3. Buttons:
   - Full width
   - Stacked vertically
   - Apply button on top

4. Active indicator:
   - Full width
   - Smaller text (12px)

---

### Step 6: Add Developer Annotations

Navigate to **📐 Specs & Annotations** page.

Create annotation section for Date Range Filter:

```
=================================
DATE RANGE FILTER COMPONENT
=================================

API Integration:
- Endpoint parameter: ?from_date=YYYY-MM&to_date=YYYY-MM
- Format: Month in YYYY-MM format
- Applies to ALL analysis endpoints:
  * /api/advanced/customers/{id}/anchor-frequency
  * /api/advanced/customers/{id}/word-frequency
  * /api/advanced/customers/{id}/target-url-analysis
  * /api/advanced/customers/{id}/link-velocity
  * /api/advanced/customers/{id}/domain-sources

State Management:
- Store in React state/context
- Persist across tab switches
- Clear button resets to "all time"

Date Picker Behavior:
- Click input → open dropdown
- Select month → close dropdown
- Year arrows: increment/decrement by 1
- Default: Last 12 months

Validation:
- "From" cannot be after "To"
- Show error if invalid range
- Max range: No limit (allow full history)

UI Feedback:
- Apply button: disabled until valid dates selected
- Clear button: only shown when filter active
- Active indicator: shows current range in readable format
- Toast on apply: "Filter applied: Jan 2024 - Dec 2024"

Responsive:
- Desktop (1200px+): Horizontal layout
- Tablet (768-1199px): Horizontal with wrapping
- Mobile (<768px): Vertical stack
```

---

### Step 7: Create Prototype Interactions

Navigate to **Prototype** mode in Figma.

#### 7.1 DatePicker Interactions

**On Click (DatePicker input):**
- Action: Open overlay
- Target: DatePickerDropdown
- Animation: Fade in (200ms)
- Position: Below input, aligned left

**On Click (Month cell):**
- Action: Close overlay
- Animation: Fade out (150ms)
- Change To: Selected state

**On Click (Year arrows):**
- Action: Change year text
- Animation: Slide (100ms)

#### 7.2 DateRangeFilter Interactions

**On Click (Apply Button):**
- Action: Change variant
- Target: DateRangeFilter
- Change To: Active state
- Animation: Instant

**On Click (Clear Button or X icon):**
- Action: Change variant
- Target: DateRangeFilter
- Change To: Inactive state
- Animation: Instant

**On Click (Active indicator X):**
- Same as Clear button

---

### Step 8: Create Usage Examples

Navigate to **📐 Specs & Annotations** page.

Add visual examples:

#### Example 1: Default State
**Screenshot of filter in inactive state**
- Caption: "Filter inactive - showing all time data"

#### Example 2: Selecting Date
**Screenshot of dropdown open**
- Caption: "User selecting month from picker"

#### Example 3: Active Filter
**Screenshot of filter in active state**
- Caption: "Filter applied - data filtered to Jan-Dec 2024"

#### Example 4: Mobile View
**Screenshot of mobile layout**
- Caption: "Vertical layout on mobile devices"

---

## ✅ Implementation Checklist

Complete these tasks in order:

**Components:**
- [ ] Create DatePicker component (input + dropdown)
- [ ] Create month grid in dropdown (3×4 layout)
- [ ] Create year selector with arrows
- [ ] Create DatePicker variants (Light/Dark, Empty/Selected)
- [ ] Create DateRangeFilter container
- [ ] Add From and To date pickers
- [ ] Add Apply and Clear buttons
- [ ] Create active filter indicator
- [ ] Create DateRangeFilter variants (4 total)

**Page Integration:**
- [ ] Add to Customer Analysis page (Light mode)
- [ ] Position between metrics and tabs
- [ ] Create "filtered" version of page
- [ ] Add to Customer Analysis page (Dark mode)
- [ ] Test visibility and alignment

**Responsive:**
- [ ] Create tablet layout (vertical wrap)
- [ ] Create mobile layout (full vertical)
- [ ] Test all breakpoints
- [ ] Ensure touch targets are 44px minimum

**Prototyping:**
- [ ] Add click interactions to open/close dropdown
- [ ] Add month selection interactions
- [ ] Add Apply/Clear button interactions
- [ ] Test prototype flow

**Documentation:**
- [ ] Add developer annotations
- [ ] Document API parameters
- [ ] Add usage examples
- [ ] Include state management notes

---

## 🎯 Success Criteria

Your implementation is complete when:

1. ✅ DatePicker component works in both light and dark modes
2. ✅ Dropdown shows month grid and year selector correctly
3. ✅ DateRangeFilter shows From/To pickers with arrow between
4. ✅ Active filter indicator appears when filter is applied
5. ✅ Component is integrated into Customer Analysis page
6. ✅ Responsive layouts work on all screen sizes
7. ✅ Prototype interactions demonstrate the flow
8. ✅ Developer annotations are clear and complete

---

## 📊 Visual Reference

```
DESKTOP LAYOUT (Light Mode):
┌────────────────────────────────────────────────────────────────────┐
│  Filter by Date Range                                              │
│                                                                     │
│  From          To                                                  │
│  [2024-01 ▾]  [2024-12 ▾]  [Apply Filter]  [Clear]   📅 Jan-Dec'24│
└────────────────────────────────────────────────────────────────────┘

DROPDOWN VIEW:
┌──────────────┐
│  2024   ◄ ►  │
├──────────────┤
│ Jan Feb Mar  │
│ Apr May Jun  │
│ Jul Aug Sep  │
│ Oct Nov Dec  │
└──────────────┘

MOBILE LAYOUT:
┌──────────────┐
│ Filter Range │
│              │
│ From         │
│ [2024-01 ▾]  │
│              │
│ To           │
│ [2024-12 ▾]  │
│              │
│ [Apply]      │
│ [Clear]      │
│              │
│ 📅 Jan-Dec   │
└──────────────┘
```

---

## 🔗 Related Addons

This addon works with:
- **FIGMA_ADDON_ENHANCED_ANCHOR.md** - Anchor analysis uses date filter
- **FIGMA_ADDON_ANALYSIS_TABS_1.md** - Velocity and target URL tabs use filter
- **FIGMA_ADDON_ANALYSIS_TABS_2.md** - Domain and comparison tabs use filter

---

**Version:** 1.0
**Estimated Time:** 20-30 minutes
**Difficulty:** ⭐⭐ Intermediate
**Dependencies:** FIGMA_DESIGN_PROMPT.md (Phases 1-15)
