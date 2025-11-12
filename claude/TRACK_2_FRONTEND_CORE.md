# TRACK 2: Frontend Core & Layout [2/5]

**Agent:** Frontend Architect
**Status:** Ready to Execute
**Credits:** Part of $150 budget (Claude Code)
**Estimated Time:** 2-3 hours

---

## 🎯 Mission

Du är **Track 2** i ett 5-track parallellt utvecklingsteam. Din uppgift är att bygga React-applikationens core structure, routing och layout components.

**KRITISKT:** De andra 4 tracks arbetar samtidigt. Följ dina boundaries exakt!

---

## 🚦 Boundary Rules

### ✅ DU FÅR RÖRA:
```
gui/frontend/
├── package.json                    # Dependencies
├── tailwind.config.js              # Tailwind setup
├── vite.config.js                  # Vite config (eller webpack)
├── index.html
├── src/
│   ├── App.jsx                     # Main app + routing
│   ├── main.jsx                    # Entry point
│   ├── index.css                   # Global styles + Tailwind
│   ├── components/
│   │   ├── layout/                 # DIN HUVUDFOKUS!
│   │   │   ├── Layout.jsx          # Main layout wrapper
│   │   │   ├── Sidebar.jsx         # Navigation sidebar
│   │   │   ├── Header.jsx          # Top header
│   │   │   └── Footer.jsx          # Optional footer
│   │   └── common/                 # Reusable components
│   │       ├── Button.jsx
│   │       ├── Card.jsx
│   │       ├── Badge.jsx
│   │       ├── LoadingSpinner.jsx
│   │       └── ErrorBoundary.jsx
│   └── styles/
│       └── theme.js                # Color constants, spacing
```

### ❌ DU FÅR INTE RÖRA:
- `gui/frontend/src/pages/` - Track 4 gör pages
- `gui/frontend/src/components/charts/` - Track 3 gör charts
- `gui/frontend/src/utils/` - Track 5 gör utils
- `gui/frontend/src/hooks/` - Track 5 gör hooks
- `gui/backend/` - Track 1 gör backend

---

## 👥 Vad de Andra Tracks Gör (Rör EJ!)

| Track | Ansvar | Directory |
|-------|--------|-----------|
| **Track 1** | Backend API | `gui/backend/` |
| **Track 3** | Charts & Visualizations | `gui/frontend/src/components/charts/` |
| **Track 4** | Pages & Views | `gui/frontend/src/pages/` |
| **Track 5** | Utils & Hooks | `gui/frontend/src/utils/`, `gui/frontend/src/hooks/` |

**Track 4 förväntar sig att du levererar:**
- Fungerande routing
- Layout struktur de kan använda
- Common components de kan importera

**Track 3 & 4 förväntar sig:**
- Tailwind konfigurerad
- Design system färgschema
- Common components redo

---

## 📋 Din Uppgift

### Del 1: Project Setup (30 min)

1. **Initialize React + Vite:**
   ```bash
   cd gui
   npm create vite@latest frontend -- --template react
   cd frontend
   npm install
   ```

2. **Install dependencies:**
   ```bash
   npm install react-router-dom
   npm install tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   npm install lucide-react  # För icons
   ```

3. **Configure Tailwind** (`tailwind.config.js`):
   ```js
   /** @type {import('tailwindcss').Config} */
   export default {
     content: [
       "./index.html",
       "./src/**/*.{js,ts,jsx,tsx}",
     ],
     theme: {
       extend: {
         colors: {
           primary: {
             50: '#eff6ff',
             100: '#dbeafe',
             200: '#bfdbfe',
             300: '#93c5fd',
             400: '#60a5fa',
             500: '#3b82f6',  // Main primary
             600: '#2563eb',
             700: '#1d4ed8',
             800: '#1e40af',
             900: '#1e3a8a',
           },
           success: '#10b981',
           warning: '#f59e0b',
           danger: '#ef4444',
         },
         fontFamily: {
           sans: ['Inter', 'system-ui', 'sans-serif'],
         },
       },
     },
     plugins: [],
   }
   ```

4. **Setup global styles** (`src/index.css`):
   ```css
   @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

   @tailwind base;
   @tailwind components;
   @tailwind utilities;

   @layer base {
     body {
       @apply bg-gray-50 text-gray-900;
     }
   }
   ```

### Del 2: Theme Constants (15 min)

**Fil:** `src/styles/theme.js`

```js
export const colors = {
  primary: {
    main: '#2563eb',
    light: '#60a5fa',
    dark: '#1e40af',
  },
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    700: '#374151',
    900: '#111827',
  },
};

export const spacing = {
  xs: '0.25rem',
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
};

export const borderRadius = {
  sm: '0.25rem',
  md: '0.5rem',
  lg: '0.75rem',
  xl: '1rem',
};
```

### Del 3: Common Components (60 min)

#### 3.1 Button Component
**Fil:** `src/components/common/Button.jsx`

```jsx
import React from 'react';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  disabled = false,
  className = ''
}) => {
  const baseClasses = 'font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
```

#### 3.2 Card Component
**Fil:** `src/components/common/Card.jsx`

```jsx
import React from 'react';

const Card = ({ children, title, subtitle, className = '' }) => {
  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {title && (
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {subtitle && <p className="text-sm text-gray-600 mt-1">{subtitle}</p>}
        </div>
      )}
      {children}
    </div>
  );
};

export default Card;
```

#### 3.3 Badge Component
**Fil:** `src/components/common/Badge.jsx`

```jsx
import React from 'react';

const Badge = ({ children, variant = 'default' }) => {
  const variantClasses = {
    default: 'bg-gray-100 text-gray-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
    info: 'bg-blue-100 text-blue-800',
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${variantClasses[variant]}`}>
      {children}
    </span>
  );
};

export default Badge;
```

#### 3.4 LoadingSpinner Component
**Fil:** `src/components/common/LoadingSpinner.jsx`

```jsx
import React from 'react';

const LoadingSpinner = ({ size = 'md' }) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  return (
    <div className="flex justify-center items-center">
      <div className={`animate-spin rounded-full border-b-2 border-blue-600 ${sizeClasses[size]}`}></div>
    </div>
  );
};

export default LoadingSpinner;
```

#### 3.5 ErrorBoundary Component
**Fil:** `src/components/common/ErrorBoundary.jsx`

```jsx
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-red-600 mb-4">Oops!</h1>
            <p className="text-gray-700 mb-4">Something went wrong.</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

### Del 4: Layout Components (90 min)

#### 4.1 Sidebar Component
**Fil:** `src/components/layout/Sidebar.jsx`

```jsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Users,
  Trophy,
  Link as LinkIcon,
  Settings
} from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/customers', icon: Users, label: 'Customers' },
    { path: '/competitive', icon: Trophy, label: 'Competitive' },
    { path: '/links', icon: LinkIcon, label: 'Link Explorer' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="w-64 bg-gray-900 min-h-screen text-white flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-800">
        <h1 className="text-2xl font-bold">LinkDB</h1>
        <p className="text-sm text-gray-400">Analytics</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  }`}
                >
                  <Icon size={20} />
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-800 text-sm text-gray-400">
        <p>Version 1.0</p>
        <p>© 2025 LinkDB</p>
      </div>
    </div>
  );
};

export default Sidebar;
```

#### 4.2 Header Component
**Fil:** `src/components/layout/Header.jsx`

```jsx
import React from 'react';
import { Bell, User, Search } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Search Bar */}
        <div className="flex-1 max-w-lg">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Search customers, links..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Right Side Actions */}
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <button className="relative p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
            <Bell size={20} />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* User Menu */}
          <button className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <User size={16} className="text-white" />
            </div>
            <span className="text-sm font-medium text-gray-700">Admin</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
```

#### 4.3 Main Layout Component
**Fil:** `src/components/layout/Layout.jsx`

```jsx
import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

const Layout = ({ children }) => {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
```

### Del 5: App & Routing Setup (30 min)

#### 5.1 Main App Component
**Fil:** `src/App.jsx`

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import ErrorBoundary from './components/common/ErrorBoundary';

// Placeholder pages (Track 4 will create real ones)
const Dashboard = () => (
  <div>
    <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
    <p className="text-gray-600">Track 4 will build this page</p>
  </div>
);

const Customers = () => (
  <div>
    <h1 className="text-3xl font-bold mb-4">Customers</h1>
    <p className="text-gray-600">Track 4 will build this page</p>
  </div>
);

const Competitive = () => (
  <div>
    <h1 className="text-3xl font-bold mb-4">Competitive Benchmarking</h1>
    <p className="text-gray-600">Track 4 will build this page</p>
  </div>
);

const LinkExplorer = () => (
  <div>
    <h1 className="text-3xl font-bold mb-4">Link Explorer</h1>
    <p className="text-gray-600">Track 4 will build this page</p>
  </div>
);

const Settings = () => (
  <div>
    <h1 className="text-3xl font-bold mb-4">Settings</h1>
    <p className="text-gray-600">Track 4 will build this page</p>
  </div>
);

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/customers/:id" element={<div>Customer Detail - Track 4</div>} />
            <Route path="/competitive" element={<Competitive />} />
            <Route path="/links" element={<LinkExplorer />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
```

#### 5.2 Entry Point
**Fil:** `src/main.jsx`

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

---

## 📊 Deliverables Checklist

- [ ] React + Vite project initialized
- [ ] Tailwind CSS configured
- [ ] Design system theme setup
- [ ] Common components created (Button, Card, Badge, LoadingSpinner, ErrorBoundary)
- [ ] Sidebar component with navigation
- [ ] Header component with search
- [ ] Main Layout component
- [ ] Routing setup (React Router)
- [ ] App starts without errors: `npm run dev`
- [ ] All navigation links work
- [ ] Responsive layout (desktop minimum)

---

## 🎯 Success Criteria

1. **Dev server starts:**
   ```bash
   cd gui/frontend
   npm run dev
   # Opens on http://localhost:5173
   ```

2. **Navigation works:**
   - Click sidebar items
   - URL changes
   - Active state highlights correct item

3. **Layout looks professional:**
   - Sidebar fixed left
   - Header fixed top
   - Content scrollable
   - Colors match design system

4. **Components render:**
   - Button with different variants
   - Card with title
   - Badge with colors
   - LoadingSpinner animates

5. **No console errors!**

---

## 🔄 Handoff to Other Tracks

När du är klar, skapa: `gui/frontend/FRONTEND_SETUP.md`

**Innehåll:**
```markdown
# Frontend Setup Complete

## Available Components

### Layout
- `Layout` - Main layout wrapper
- `Sidebar` - Navigation sidebar
- `Header` - Top header

### Common
- `Button` - Button component
- `Card` - Card container
- `Badge` - Status badge
- `LoadingSpinner` - Loading indicator
- `ErrorBoundary` - Error handling

## How to Use

Import components:
```jsx
import Layout from './components/layout/Layout';
import Button from './components/common/Button';
```

## Routing

Routes defined in `App.jsx`:
- `/` - Dashboard
- `/customers` - Customer list
- `/customers/:id` - Customer detail
- `/competitive` - Competitive page
- `/links` - Link explorer
- `/settings` - Settings

## Design System

Colors in `src/styles/theme.js`

## Start Dev Server

```bash
cd gui/frontend
npm run dev
```
```

---

## 🎬 Ready to Start?

1. **Open Claude Code**
2. **Load this file:** `TRACK_2_FRONTEND_CORE.md`
3. **Tell Claude Code:**
   ```
   Execute TRACK_2_FRONTEND_CORE.md

   You are Track 2 of 5 parallel development tracks.
   Build the React frontend core: layout, routing, common components.
   DO NOT build pages - Track 4 does that.
   DO NOT build charts - Track 3 does that.

   Setup React, Tailwind, routing, and layout components.
   Create placeholder pages for Track 4 to replace.

   When done, create FRONTEND_SETUP.md for other tracks.
   ```

4. **Let it run!**

---

**Track 2 skapar fundamentet för hela frontend!** 🎨

*Estimated completion: 2-3 hours*
*Budget: ~$20-30 of $150 credits*
