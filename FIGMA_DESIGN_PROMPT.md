# LinkDB GUI - Figma Design System Prompt

## 📋 Overview
LinkDB is a professional SEO link analysis dashboard built with React, Tailwind CSS, and modern data visualization. The system includes light/dark mode support, AI-powered insights, and comprehensive analytics features.

---

## 🎨 Design System Foundation

### Color Palette

#### Light Mode
```
Primary Colors:
- Primary Blue: #2563EB (blue-600)
- Primary Blue Hover: #1D4ED8 (blue-700)
- Focus Ring: #3B82F6 (blue-500)

Background Colors:
- Page Background: #F3F4F6 (gray-100)
- Card Background: #FFFFFF (white)
- Hover Background: #F9FAFB (gray-50)
- Secondary Background: #F3F4F6 (gray-100)

Text Colors:
- Primary Text: #111827 (gray-900)
- Secondary Text: #4B5563 (gray-700)
- Muted Text: #6B7280 (gray-600)
- Disabled Text: #9CA3AF (gray-400)

Border Colors:
- Default Border: #E5E7EB (gray-200)
- Input Border: #D1D5DB (gray-300)
- Divider: #E5E7EB (gray-200)

Status Colors:
- Success: #10B981 (green-500) / #D1FAE5 (green-100 bg)
- Warning: #F59E0B (amber-500) / #FEF3C7 (yellow-100 bg)
- Danger: #EF4444 (red-500) / #FEE2E2 (red-100 bg)
- Info: #3B82F6 (blue-500) / #DBEAFE (blue-100 bg)
```

#### Dark Mode
```
Primary Colors:
- Primary Blue: #3B82F6 (blue-600)
- Primary Blue Hover: #2563EB (blue-700)
- Focus Ring: #60A5FA (blue-400)

Background Colors:
- Page Background: #111827 (gray-900)
- Card Background: #1F2937 (gray-800)
- Hover Background: rgba(55, 65, 81, 0.5) (gray-700/50)
- Secondary Background: rgba(31, 41, 55, 0.5) (gray-800/50)
- Elevated Background: #030712 (gray-950)

Text Colors:
- Primary Text: #F9FAFB (gray-100)
- Secondary Text: #D1D5DB (gray-300)
- Muted Text: #9CA3AF (gray-400)
- Disabled Text: #6B7280 (gray-600)

Border Colors:
- Default Border: #374151 (gray-700)
- Input Border: #4B5563 (gray-600)
- Divider: #374151 (gray-700)

Status Colors (Dark Mode Variants):
- Success: #34D399 (green-400) / rgba(6, 78, 59, 0.3) (green-900/30 bg)
- Warning: #FBBF24 (yellow-400) / rgba(120, 53, 15, 0.3) (yellow-900/30 bg)
- Danger: #F87171 (red-400) / rgba(127, 29, 29, 0.3) (red-900/30 bg)
- Info: #60A5FA (blue-400) / rgba(30, 58, 138, 0.3) (blue-900/30 bg)
```

### Typography

```
Font Family:
- System Font Stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif

Font Sizes:
- xs: 12px (0.75rem) - Small labels, badges
- sm: 14px (0.875rem) - Secondary text, table cells
- base: 16px (1rem) - Body text, inputs
- lg: 18px (1.125rem) - Large body text
- xl: 20px (1.25rem) - Subheadings
- 2xl: 24px (1.5rem) - Card titles, metrics
- 3xl: 30px (1.875rem) - Page headers
- 4xl: 36px (2.25rem) - Hero text

Font Weights:
- Regular: 400 - Body text
- Medium: 500 - Labels, buttons
- Semibold: 600 - Card titles, table headers
- Bold: 700 - Page titles, metrics

Line Heights:
- Tight: 1.25 - Headings
- Normal: 1.5 - Body text
- Relaxed: 1.625 - Large text blocks
```

### Spacing System (Tailwind Standard)

```
Spacing Scale (in px):
- 1: 4px
- 2: 8px
- 3: 12px
- 4: 16px
- 5: 20px
- 6: 24px
- 8: 32px
- 10: 40px
- 12: 48px
- 16: 64px
- 20: 80px
- 24: 96px

Common Usage:
- Component Padding: 24px (p-6)
- Card Padding: 24px (p-6)
- Section Margin: 24px (mb-6)
- Button Padding: 16px horizontal, 8px vertical (px-4 py-2)
- Input Padding: 16px horizontal, 8px vertical (px-4 py-2)
```

### Border Radius

```
- sm: 4px (rounded-sm) - Badges, small elements
- DEFAULT: 8px (rounded-lg) - Cards, buttons, inputs
- md: 6px (rounded-md) - Alternative medium
- lg: 8px (rounded-lg) - Default for most components
- full: 9999px (rounded-full) - Pills, badges, avatars
```

### Shadows

```
Light Mode:
- Card Shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)
- Hover Shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)

Dark Mode:
- Card Shadow: 0 1px 3px 0 rgb(0 0 0 / 0.5), 0 1px 2px -1px rgb(0 0 0 / 0.5)
- Hover Shadow: Same as light mode
```

---

## 🧩 Component Library

### 1. Layout Components

#### **Header**
```
Dimensions:
- Height: Auto (content-based)
- Padding: 16px horizontal, 16px vertical

Structure (Left to Right):
1. Logo Area (Optional):
   - Size: 40px × 40px
   - Margin-right: 16px

2. Title Section:
   - Font: 20px, Semibold
   - Color: gray-800 (light) / gray-100 (dark)
   - Text: "Analytics Dashboard" (or dynamic page title)

3. Spacer (flex-1)

4. Theme Toggle Button:
   - Size: 40px × 40px
   - Background: gray-200 (light) / gray-700 (dark)
   - Icon: Moon (light mode) / Sun (dark mode)
   - Icon Size: 20px × 20px
   - Hover: gray-300 (light) / gray-600 (dark)
   - Transition: All 200ms

Styling:
- Background: white (light) / gray-800 (dark)
- Border-bottom: 1px solid gray-200 (light) / gray-700 (dark)
- Shadow: Default card shadow
- Transition: Colors 200ms
```

#### **Sidebar**
```
Dimensions:
- Width: 256px (16rem)
- Height: 100vh
- Position: Fixed left

Structure (Top to Bottom):
1. Logo/Brand Section:
   - Height: 80px
   - Padding: 24px
   - Content: "🔗 LinkDB" or logo
   - Font: 20px, Bold
   - Color: white
   - Border-bottom: 1px solid gray-700 (light) / gray-800 (dark)

2. Navigation Menu:
   - Padding: 16px

   Navigation Item (Default):
   - Height: 40px
   - Padding: 10px 16px
   - Border-radius: 8px
   - Font: 16px, Medium
   - Color: gray-400 (light) / gray-500 (dark)
   - Icon: 20px × 20px, left-aligned
   - Icon margin-right: 12px
   - Hover: gray-700 (light) / gray-800 (dark)

   Navigation Item (Active):
   - Background: gray-700 (light) / gray-800 (dark)
   - Color: white
   - Border-left: 3px solid blue-600

Navigation Items:
- 📊 Dashboard
- 👥 Customers
- 🔗 Link Explorer
- 📈 Competitive
- 🤖 AI Chat
- ⚙️ Settings

Styling:
- Background: gray-800 (light) / gray-950 (dark)
- Text: white
- Transition: All 200ms
```

#### **Main Content Area**
```
Dimensions:
- Margin-left: 256px (sidebar width)
- Padding: 32px
- Min-height: 100vh
- Background: gray-100 (light) / gray-900 (dark)

Structure:
1. Page Title:
   - Font: 30px, Bold
   - Margin-bottom: 24px
   - Color: gray-900 (light) / gray-100 (dark)

2. Content Area:
   - Cards and components flow vertically
   - Gap between sections: 24px
```

### 2. Core Components

#### **Card Component**
```
Structure:
- Background: white (light) / gray-800 (dark)
- Border-radius: 8px
- Padding: 24px
- Shadow: Default card shadow
- Transition: Colors 200ms

With Title:
- Title Font: 18px, Semibold
- Title Color: gray-900 (light) / gray-100 (dark)
- Title Margin-bottom: 16px

Variants:
- Default: As above
- Compact: Padding 16px
- Highlighted: Border-left 4px solid blue-600

Hover State:
- Shadow increases slightly
- Cursor: pointer (if clickable)
```

#### **Button Component**
```
Base Structure:
- Height: 40px (auto with py-2)
- Padding: 16px horizontal, 8px vertical
- Border-radius: 8px
- Font: 16px, Medium
- Transition: All 200ms
- Cursor: pointer

Primary Variant:
- Background: blue-600 (light) / blue-700 (dark)
- Color: white
- Hover Background: blue-700 (light) / blue-600 (dark)

Secondary Variant:
- Background: gray-200 (light) / gray-700 (dark)
- Color: gray-800 (light) / gray-200 (dark)
- Hover Background: gray-300 (light) / gray-600 (dark)

Danger Variant:
- Background: red-600 (light) / red-700 (dark)
- Color: white
- Hover Background: red-700 (light) / red-600 (dark)

Disabled State:
- Opacity: 0.5
- Cursor: not-allowed
- No hover effects
```

#### **Badge Component**
```
Structure:
- Height: 24px (auto with py-0.5)
- Padding: 10px horizontal, 2px vertical
- Border-radius: 9999px (full)
- Font: 12px, Medium
- Display: inline-flex
- Align-items: center
- Transition: Colors 200ms

Variants:

Default:
- Background: gray-100 (light) / gray-700 (dark)
- Color: gray-800 (light) / gray-200 (dark)

Success:
- Background: green-100 (light) / rgba(6, 78, 59, 0.3) (dark)
- Color: green-800 (light) / green-400 (dark)

Warning:
- Background: yellow-100 (light) / rgba(120, 53, 15, 0.3) (dark)
- Color: yellow-800 (light) / yellow-400 (dark)

Danger:
- Background: red-100 (light) / rgba(127, 29, 29, 0.3) (dark)
- Color: red-800 (light) / red-400 (dark)

Info:
- Background: blue-100 (light) / rgba(30, 58, 138, 0.3) (dark)
- Color: blue-800 (light) / blue-400 (dark)
```

#### **Input Component**
```
Structure:
- Height: 40px (auto with py-2)
- Width: 100% (or specified)
- Padding: 16px horizontal, 8px vertical
- Border: 1px solid gray-300 (light) / gray-600 (dark)
- Border-radius: 8px
- Background: white (light) / gray-700 (dark)
- Font: 16px, Regular
- Color: gray-900 (light) / gray-100 (dark)
- Placeholder Color: gray-500 (light) / gray-400 (dark)
- Transition: All 200ms

Focus State:
- Outline: None
- Ring: 2px solid blue-500 (light) / blue-400 (dark)
- Border-color: blue-500 (light) / blue-400 (dark)

Disabled State:
- Background: gray-100 (light) / gray-800 (dark)
- Cursor: not-allowed
- Opacity: 0.6
```

#### **Table Component**
```
Structure:

Table Container:
- Width: 100%
- Overflow-x: auto (for responsiveness)

Table:
- Width: 100%
- Border-collapse: collapse

Table Header (thead):
- Border-bottom: 1px solid gray-200 (light) / gray-700 (dark)

Table Header Cell (th):
- Text-align: left
- Padding: 12px 16px
- Font: 14px, Semibold
- Color: gray-700 (light) / gray-300 (dark)

Table Row (tr):
- Border-bottom: 1px solid gray-200 (light) / gray-700 (dark)
- Hover Background: gray-50 (light) / rgba(55, 65, 81, 0.5) (dark)
- Transition: Background 200ms
- Cursor: pointer (if clickable)

Table Cell (td):
- Padding: 12px 16px
- Font: 14px, Regular
- Color: gray-700 (light) / gray-300 (dark)

Table Cell (Primary):
- Font-weight: Medium
- Color: gray-900 (light) / gray-100 (dark)
```

#### **Loading Spinner**
```
Structure:
- Size:
  - Small: 16px × 16px
  - Medium: 32px × 32px
  - Large: 48px × 48px
- Border-width: 4px
- Border-color: blue-200 (light) / blue-900 (dark)
- Border-top-color: blue-600 (light) / blue-400 (dark)
- Border-radius: 50%
- Animation: Spin 1s linear infinite

Container:
- Display: flex
- Justify-content: center
- Align-items: center
- Height: 256px (for page loaders)
```

#### **Empty State**
```
Structure:
- Display: flex
- Flex-direction: column
- Align-items: center
- Justify-content: center
- Padding: 48px vertical

Icon:
- Font-size: 60px (emoji or icon)
- Margin-bottom: 16px

Message:
- Font: 18px, Regular
- Color: gray-600 (light) / gray-400 (dark)
- Text-align: center
```

#### **Tab Navigation**
```
Structure:

Tab Container:
- Border-bottom: 1px solid gray-200 (light) / gray-700 (dark)
- Display: flex
- Gap: 32px

Tab Button:
- Padding: 16px vertical, 8px horizontal
- Border-bottom: 2px solid transparent
- Font: 16px, Medium
- Color: gray-600 (light) / gray-400 (dark)
- Transition: All 200ms
- Cursor: pointer

Tab Button (Active):
- Border-bottom-color: blue-600 (light) / blue-400 (dark)
- Color: blue-600 (light) / blue-400 (dark)

Tab Button (Hover):
- Color: gray-900 (light) / gray-200 (dark)
```

### 3. Specialized Components

#### **Health Gauge (Circular Progress)**
```
Structure:
- Size: Variable (80px, 150px common)
- SVG-based circular progress indicator

Components:
1. Background Circle:
   - Stroke: gray-200 (light) / gray-700 (dark)
   - Stroke-width: 8
   - Fill: none

2. Progress Circle:
   - Stroke: Color based on score
     - 0-50: red-500
     - 51-75: yellow-500
     - 76-100: green-500
   - Stroke-width: 8
   - Fill: none
   - Stroke-linecap: round
   - Animation: Progress fill

3. Center Text:
   - Font: 24px, Bold (for 150px size)
   - Color: gray-900 (light) / gray-100 (dark)
   - Content: Score number (e.g., "85")
```

#### **KPI Metric Card**
```
Structure (Inside Card):
- Display: flex
- Justify-content: space-between
- Align-items: center

Left Section:
1. Label:
   - Font: 14px, Regular
   - Color: gray-600 (light) / gray-400 (dark)
   - Margin-bottom: 8px

2. Value:
   - Font: 30px, Bold
   - Color: gray-900 (light) / gray-100 (dark)

Right Section:
- Icon/Visual:
  - Size: 48px × 48px (for emoji)
  - Or Health Gauge (80px × 80px)
```

#### **AI Chat Component**
```
Structure:

Container:
- Background: white (light) / gray-800 (dark)
- Border-radius: 8px
- Padding: 24px
- Min-height: 600px
- Display: flex
- Flex-direction: column

Messages Container:
- Flex: 1
- Overflow-y: auto
- Padding: 16px
- Gap: 16px

Message Bubble (User):
- Background: blue-600
- Color: white
- Border-radius: 8px (with 2px on bottom-right for tail effect)
- Padding: 12px 16px
- Max-width: 70%
- Align-self: flex-end
- Font: 16px, Regular

Message Bubble (AI):
- Background: gray-100 (light) / gray-700 (dark)
- Color: gray-900 (light) / gray-100 (dark)
- Border-radius: 8px (with 2px on bottom-left for tail effect)
- Padding: 12px 16px
- Max-width: 70%
- Align-self: flex-start
- Font: 16px, Regular

Input Area:
- Border-top: 1px solid gray-200 (light) / gray-700 (dark)
- Padding-top: 16px
- Display: flex
- Gap: 8px

Input Field:
- Flex: 1
- (Use standard input styling)

Send Button:
- (Use primary button styling)
- Icon: Send arrow
```

#### **Insights Panel (AI)**
```
Structure:

Container (Card-based):
- Gradient background:
  - Light: from-blue-50 to-purple-50
  - Dark: from-blue-900/20 to-purple-900/20
- Border: blue-200 (light) / blue-800 (dark)
- Border-radius: 8px
- Padding: 20px

Header:
1. Icon: 🔍 or lightbulb
   - Size: 24px
   - Margin-bottom: 8px

2. Title:
   - Font: 18px, Semibold
   - Color: blue-900 (light) / blue-300 (dark)

Content:
- List of insights
- Each insight:
  - Padding: 12px
  - Background: white/10 (light) / black/10 (dark)
  - Border-radius: 6px
  - Margin-bottom: 8px
  - Font: 14px, Regular
  - Color: blue-800 (light) / blue-400 (dark)
```

---

## 📱 Page Layouts

### **Dashboard Page**

```
Layout Structure:

1. Page Title
   - "Dashboard"
   - Font: 30px, Bold
   - Margin-bottom: 24px

2. KPI Cards Row
   - Grid: 3 columns (1 on mobile)
   - Gap: 24px
   - Cards:
     a. Total Customers
     b. Total Links
     c. Average Health (with gauge)

3. Top Performers Table Card
   - Full width
   - Margin-top: 24px
   - Contains table with:
     - Rank
     - Customer name
     - Links count
```

### **Customer List Page**

```
Layout Structure:

1. Page Title
   - "Customers"
   - Font: 30px, Bold
   - Margin-bottom: 24px

2. Search Card
   - Full width
   - Contains search input
   - Placeholder: "Search customers..."
   - Margin-bottom: 24px

3. Customers Table Card
   - Full width
   - Columns:
     - Customer (domain)
     - Brand
     - Links (count)
     - Health Score (number)
     - Status (badge)
```

### **Customer Analysis Page**

```
Layout Structure:

1. Header Section
   - Customer domain name (h1)
   - Brand name (subtitle)
   - Margin-bottom: 24px

2. Executive Summary Card
   - Overall Health Badge
   - Health Gauge (150px)
   - Margin-bottom: 24px

3. Key Metrics Row
   - Grid: 3 columns
   - Gap: 24px
   - Cards:
     a. Anchor Quality
     b. Temporal Health
     c. Domain Quality

4. Tab Navigation
   - Tabs:
     - Overview
     - Anchor Analysis
     - Temporal Patterns
     - Domain Quality
     - Competitive
     - 🤖 AI Assistant
   - Margin-bottom: 24px

5. Tab Content Area
   - Dynamic based on active tab
   - Full width

Tab: Overview
- Link Portfolio Card (4-column grid of stats)
- Top Recommendations Card
- AI Insights Grid (2 columns: Insights Panel + Recommendations Card)

Tab: Anchor Analysis
- Anchor Quality Overview Card (4-column metrics grid)
- Anchor Distribution Chart (Pie chart)
- Warnings Card (if applicable)

Tab: Temporal Patterns
- Temporal Health Card (4-column metrics grid)
- Monthly Distribution Chart (Bar chart)

Tab: Domain Quality
- Domain Quality Card (4-column metrics grid)
- TLD Distribution Chart

Tab: AI Assistant
- Full-width AI Chat Component
```

### **Link Explorer Page**

```
Layout Structure:

1. Page Title
   - "Link Explorer"
   - Font: 30px, Bold
   - Margin-bottom: 24px

2. Search & Filters Card
   - Full width
   - Contains:
     - Search input (flex-grow)
     - Export CSV button
     - Export JSON button
   - Margin-bottom: 24px

3. Links Table Card
   - Full width
   - Columns:
     - Customer
     - Pub Domain
     - Target URL
     - Anchor Text
     - Type (badge)
     - Date

4. Pagination
   - Inside table card
   - Border-top
   - Padding-top: 16px
   - Display: flex
   - Justify-content: space-between
   - Left: "Showing X-Y of Z links"
   - Right: Previous/Next buttons
```

### **Competitive Benchmarking Page**

```
Layout Structure:

1. Page Title
   - "Competitive Benchmarking"
   - Font: 30px, Bold
   - Margin-bottom: 24px

2. Industry Overview Row
   - Grid: 4 columns (2 on tablet, 1 on mobile)
   - Gap: 24px
   - Cards:
     a. Total Customers
     b. Avg Links/Customer
     c. Median Links
     d. Avg Quality

3. Scatter Plot Card
   - Full width
   - Title: "Customer Distribution"
   - Contains scatter plot chart
   - Margin-top: 24px

4. Leaderboards Row
   - Grid: 2 columns (1 on mobile)
   - Gap: 24px
   - Cards:
     a. Top 10 by Volume
     b. Top 10 by Quality
   - Each entry:
     - Rank number
     - Customer name
     - Metric value
     - Hover effect
```

### **AI Chat Page**

```
Layout Structure:

Max-width container: 1024px (centered)

1. Hero Section
   - Gradient text title: "🤖 AI SEO Assistant"
   - Font: 36px, Bold
   - Subtitle in Swedish
   - Margin-bottom: 24px

2. AI Chat Component
   - Full width
   - Height: 600px minimum

3. Feature Cards Row
   - Grid: 3 columns (1 on mobile)
   - Gap: 16px
   - Margin-top: 32px
   - Cards with gradient backgrounds:
     a. Dataanalys (Blue gradient)
     b. Strategiråd (Purple gradient)
     c. Riskdetektering (Green gradient)

4. Tip Banner
   - Full width
   - Yellow background
   - Margin-top: 24px
   - Contains tips text with icon
```

### **Settings Page**

```
Layout Structure:

1. Page Title
   - "Settings"
   - Font: 30px, Bold
   - Margin-bottom: 24px

2. Settings Cards (Stacked)
   - Full width
   - Gap: 24px
   - Cards:
     a. Database Configuration
        - Description text
        - Configure button
     b. Analysis Thresholds
        - Description text
        - Edit Thresholds button
```

---

## 📊 Chart Components

### **Pie Chart (Anchor Distribution)**
```
- Library: Recharts
- Size: Responsive (min 300px height)
- Colors:
  - Blue: #3B82F6
  - Purple: #8B5CF6
  - Green: #10B981
  - Yellow: #F59E0B
  - Red: #EF4444
- Legend: Bottom-aligned
- Labels: Percentage on hover
- Animation: Fade in
```

### **Bar Chart (Monthly Distribution)**
```
- Library: Recharts
- Size: Responsive (min 300px height)
- Bar Color: Blue-600 (light) / Blue-500 (dark)
- Grid: Horizontal lines, gray-200 (light) / gray-700 (dark)
- Axis Color: gray-400 (light) / gray-500 (dark)
- Tooltip: White background (light) / gray-800 (dark)
- Animation: Slide up
```

### **Scatter Plot (Competitive)**
```
- Library: Recharts
- Size: Responsive (min 400px height)
- Point Color: Blue-500
- Point Size: 8px
- Grid: Both axes, gray-200 (light) / gray-700 (dark)
- Axis Labels: gray-600 (light) / gray-400 (dark)
- Tooltip: Shows domain name + metrics
- Current Customer: Highlighted in red-500, size 12px
```

---

## 🎯 Interaction States

### **Hover States**
```
Buttons:
- Background color darkens/lightens
- Cursor: pointer
- Transition: 200ms

Cards:
- Shadow increases (if clickable)
- Cursor: pointer (if clickable)
- Transition: 200ms

Table Rows:
- Background: gray-50 (light) / gray-700/50 (dark)
- Cursor: pointer
- Transition: 200ms

Links/Navigation:
- Color changes to darker/lighter variant
- Transition: 200ms
```

### **Focus States**
```
Inputs:
- Ring: 2px solid blue-500 (light) / blue-400 (dark)
- Border: blue-500 (light) / blue-400 (dark)
- Outline: none

Buttons:
- Ring: 2px solid blue-500 (light) / blue-400 (dark)
- Outline: none
```

### **Active States**
```
Buttons:
- Scale: 0.98 (pressed effect)
- Transition: 100ms

Navigation Items:
- Background: Highlighted color
- Border-left: 3px solid primary color
```

### **Disabled States**
```
All Interactive Elements:
- Opacity: 0.5
- Cursor: not-allowed
- No hover effects
```

---

## 📐 Responsive Breakpoints

```
Mobile: 0px - 639px
- Sidebar: Hidden (hamburger menu)
- Grids: 1 column
- Padding: 16px
- Font sizes: Reduced by ~10%

Tablet: 640px - 1023px
- Sidebar: Collapsible or overlay
- Grids: 2 columns (where applicable)
- Padding: 24px

Desktop: 1024px+
- Full sidebar visible
- Grids: 3-4 columns
- Padding: 32px
```

---

## 🎨 Figma-Specific Instructions

### **Creating the Design System**

1. **Create Color Styles**
   ```
   For each color in the palette:
   - Create both light and dark variants
   - Name format: "Light/Primary/Blue-600" or "Dark/Primary/Blue-400"
   - Organize in folders: Primary, Background, Text, Border, Status
   ```

2. **Create Text Styles**
   ```
   For each typography definition:
   - Name format: "Heading/H1", "Body/Regular", "Label/Medium"
   - Include font family, size, weight, line-height
   - Create both light and dark color variants
   ```

3. **Create Component Variants**
   ```
   Each component should have variants for:
   - Theme: Light, Dark
   - State: Default, Hover, Focus, Disabled (where applicable)
   - Size: Small, Medium, Large (where applicable)
   - Type: Primary, Secondary, etc. (where applicable)

   Example: Button component
   - Variant properties:
     - Theme: Light/Dark
     - Type: Primary/Secondary/Danger
     - State: Default/Hover/Focus/Disabled
   ```

4. **Auto Layout Usage**
   ```
   Apply auto layout to:
   - All container components (Card, Header, Sidebar)
   - Button components
   - Form elements
   - Navigation items

   Settings:
   - Direction: Vertical for stacks, Horizontal for rows
   - Spacing: Use spacing scale (8px, 16px, 24px)
   - Padding: Based on component type
   - Resizing: "Hug contents" or "Fill container" as needed
   ```

5. **Create Component Set for Theme Toggle**
   ```
   Two states:
   1. Light mode icon (Moon): gray-700 icon
   2. Dark mode icon (Sun): yellow-400 icon

   Background:
   - Light: gray-200
   - Dark: gray-700

   Size: 40px × 40px, border-radius 8px
   ```

### **Page Templates**

1. **Create Master Frame Template**
   ```
   Frame size: 1440px × 1024px (desktop)

   Structure:
   - Sidebar frame: 256px × 1024px (left)
   - Main content frame: 1184px × 1024px (right)
     - Header: 1184px × 64px (top)
     - Content area: 1184px × 960px (scrollable)

   Background: Use color style "Light/Background/Page" or "Dark/Background/Page"
   ```

2. **Create Component Instances**
   ```
   - Drag component from assets
   - Apply correct variant (Light/Dark)
   - Adjust size if needed using auto layout
   - Apply content (text, icons)
   ```

3. **Create Charts as Placeholders**
   ```
   For charts (pie, bar, scatter):
   - Create rectangle frame
   - Add placeholder image or vector shapes
   - Label: "Recharts - [Chart Type]"
   - Color: Match theme background
   - Note: Add annotation with chart specifications
   ```

### **Prototyping**

1. **Theme Toggle**
   ```
   - Create two versions of same page (light/dark)
   - Add interaction on theme toggle button
   - Action: Navigate to → Other theme page
   - Animation: Dissolve, 200ms
   ```

2. **Navigation**
   ```
   - Link sidebar navigation items to respective pages
   - Animation: Instant or Smart Animate
   - Maintain scroll position: No
   ```

3. **Tab Switching**
   ```
   - Create frames for each tab content
   - Link tab buttons to respective content frames
   - Animation: Smart Animate, 200ms
   - Show active tab state
   ```

4. **Interactive Tables**
   ```
   - Add hover state variant to table rows
   - On click: Navigate to detail page (e.g., Customer Analysis)
   - Animation: Smart Animate
   ```

### **Annotations & Documentation**

Add annotations for developers:

1. **Color Notes**
   ```
   "Uses Tailwind color: bg-gray-100 dark:bg-gray-900"
   ```

2. **Spacing Notes**
   ```
   "Gap: 24px (gap-6 in Tailwind)"
   "Padding: 32px (p-8 in Tailwind)"
   ```

3. **Component Notes**
   ```
   "Component: Card"
   "Props: title (optional), children"
   "Styling: Apply transition-colors class"
   ```

4. **Interaction Notes**
   ```
   "On click: Navigate to /customers/:id"
   "Hover: bg-gray-50 dark:bg-gray-700/50"
   ```

5. **Chart Notes**
   ```
   "Chart: Recharts PieChart"
   "Data: anchor distribution (exact_match, branded, commercial)"
   "Colors: Blue (#3B82F6), Purple (#8B5CF6), Green (#10B981)"
   ```

---

## 🔧 Implementation Guidelines

### **Tailwind CSS Classes Reference**

For each design element, here are the corresponding Tailwind classes:

```css
/* Backgrounds */
.bg-white → Light mode card
.dark:bg-gray-800 → Dark mode card
.bg-gray-100 → Light mode page background
.dark:bg-gray-900 → Dark mode page background

/* Text Colors */
.text-gray-900 → Light mode primary text
.dark:text-gray-100 → Dark mode primary text
.text-gray-600 → Light mode secondary text
.dark:text-gray-400 → Dark mode secondary text

/* Borders */
.border-gray-200 → Light mode border
.dark:border-gray-700 → Dark mode border

/* Transitions */
.transition-colors → Color transitions
.duration-200 → 200ms transition

/* Shadows */
.shadow-md → Card shadow
.dark:shadow-gray-900/50 → Dark mode shadow enhancement

/* Hover States */
.hover:bg-gray-50 → Light mode hover
.dark:hover:bg-gray-700/50 → Dark mode hover

/* Spacing */
.p-6 → 24px padding
.mb-6 → 24px margin-bottom
.gap-6 → 24px gap in grid/flex

/* Grid */
.grid grid-cols-3 → 3 column grid
.gap-6 → 24px gap between items

/* Flex */
.flex justify-between items-center → Flex with space-between and center alignment
```

### **Component Import Structure**

```javascript
// Component imports for reference
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Badge from '../components/common/Badge';
import LoadingSpinner from '../components/common/LoadingSpinner';
import EmptyState from '../components/common/EmptyState';
import HealthGauge from '../components/charts/HealthGauge';
import ThemeToggle from '../components/common/ThemeToggle';
```

### **Dark Mode Implementation**

All components use Tailwind's `dark:` prefix:

```jsx
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
  {/* Content with automatic dark mode support */}
</div>
```

Theme is controlled by adding/removing `dark` class on `<html>` element.

---

## ✅ Figma Checklist

Before considering the design complete:

- [ ] All colors defined as styles (Light + Dark variants)
- [ ] All typography defined as text styles
- [ ] All components created with variants (Light/Dark, states)
- [ ] All 7 pages designed (Dashboard, Customers, Customer Analysis, Link Explorer, Competitive, AI Chat, Settings)
- [ ] Responsive layouts for Mobile (375px), Tablet (768px), Desktop (1440px)
- [ ] All interactive states documented (hover, focus, active, disabled)
- [ ] Prototype flows set up (navigation, theme toggle, tabs)
- [ ] Developer annotations added (Tailwind classes, component names)
- [ ] Chart placeholders with specifications
- [ ] Icon library defined (or note to use emoji/system icons)
- [ ] Spacing system documented and consistent
- [ ] Shadow system documented
- [ ] Export all components as separate file for development reference
- [ ] Create design spec document with measurements and spacing

---

## 🎨 Visual References

### **Overall Aesthetic**
- **Style**: Modern, clean, professional SaaS dashboard
- **Mood**: Data-driven, trustworthy, sophisticated
- **Inspiration**: Linear, Notion, Vercel Dashboard
- **Density**: Medium (not too cramped, not too spacious)
- **Focus**: Data visualization and AI insights

### **Key Visual Principles**
1. **Consistency**: All components follow same spacing, border-radius, shadow pattern
2. **Hierarchy**: Clear visual hierarchy using size, weight, color
3. **Breathing Room**: Generous whitespace (24px gaps, 24px padding)
4. **Accessibility**: High contrast text (WCAG AA compliant)
5. **Performance**: Smooth transitions (200ms), no jarring effects
6. **Dark Mode First**: Designed for long usage sessions

---

## 📦 Deliverables

When design is complete, export:

1. **Figma File**: Complete with all pages and components
2. **Component Library**: Separate file with all reusable components
3. **Design Tokens**: JSON export of colors, typography, spacing
4. **Icon Set**: All icons used (or note if using emoji)
5. **Prototype Link**: Interactive prototype for stakeholder review
6. **Developer Specs**: PDF with measurements, spacing, colors
7. **Assets**: Export any custom graphics, logos, illustrations

---

## 🚀 Next Steps After Design

Once Figma design is approved:

1. **Component Development**: Build React components matching design exactly
2. **Tailwind Configuration**: Extend tailwind.config.js with custom colors if needed
3. **Responsive Testing**: Test on real devices (mobile, tablet, desktop)
4. **Dark Mode Testing**: Verify all components in both themes
5. **Accessibility Audit**: Check keyboard navigation, screen readers
6. **Performance Optimization**: Lazy load components, optimize images
7. **User Testing**: Conduct usability tests with target users

---

## 📝 Notes

- All Swedish text should remain in Swedish (AI Chat page, etc.)
- Emoji icons are currently used (👥, 🔗, 📊, etc.) - these can be replaced with icon library if preferred
- Charts use Recharts library - design placeholders with similar aesthetics
- Theme toggle should be prominent in header
- AI components should have distinct visual treatment (gradients, special cards)
- Mobile experience should collapse sidebar to hamburger menu
- All data is mock data - design should accommodate real data variance

---

## 🎯 Success Criteria

The design is successful when:

1. ✅ A developer can implement pixel-perfect components from the design
2. ✅ Both light and dark modes are equally polished
3. ✅ All interactive states are clearly defined
4. ✅ Responsive layouts work on all screen sizes
5. ✅ Design system is consistent and scalable
6. ✅ Charts and data visualizations are clear and readable
7. ✅ AI features feel distinct but integrated
8. ✅ Overall aesthetic is modern, professional, and trustworthy

---

**Design Start Date**: [Fill in]
**Designer**: [Fill in]
**Version**: 1.0
**Last Updated**: [Auto-generated]
