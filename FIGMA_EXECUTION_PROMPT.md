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

**Stop here and confirm**: "Phase 15 complete. Design ready for handoff!"

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

---

## 🎬 Ready to Start?

**Begin with Phase 1: Color Styles**

Remember:
1. Work on ONE phase at a time
2. Follow specifications exactly
3. Confirm completion before moving forward
4. Take breaks between phases if needed

**Let's create an amazing design system! 🚀**
