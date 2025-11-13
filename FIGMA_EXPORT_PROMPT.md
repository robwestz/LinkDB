# Figma to React Export Prompt - LinkDB Analytics Dashboard

## Context: Backend Integration

This React application will integrate with an existing FastAPI backend located at `gui/backend/`. The backend provides a comprehensive analytics API for link tracking and SEO analysis.

### Backend API Overview

**Base URL**: `http://localhost:8000/api/v1`

**Key Endpoints**:
- `/customers` - List all customers with pagination
- `/customers/{id}/links` - Get customer's backlinks with filtering
- `/customers/{id}/stats` - Customer statistics and metrics
- `/customers/{id}/analysis` - Advanced analysis (growth, top publishers, anchors)
- `/dashboard/metrics` - Overview metrics for dashboard
- `/dashboard/activity` - Recent activity feed
- `/links` - All links with advanced filtering and search
- `/analysis/*` - Advanced analysis endpoints (growth, comparisons, trends)

**Authentication**: Currently none (will be added in Phase 4)

**Response Format**: All endpoints return JSON with consistent pagination structure:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 50,
  "total_pages": 2,
  "has_next": true,
  "has_prev": false
}
```

## Project Structure Requirements

Generate code with the following structure:

```
gui/frontend/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── common/          # Generic components (Button, Card, Table, etc.)
│   │   ├── layout/          # Layout components (Sidebar, Header, Footer)
│   │   ├── charts/          # Chart components (LineChart, BarChart, etc.)
│   │   └── dashboard/       # Dashboard-specific components
│   │
│   ├── pages/               # Page components (routes)
│   │   ├── Dashboard.tsx    # Main dashboard with metrics
│   │   ├── Customers.tsx    # Customer list page
│   │   ├── CustomerDetail.tsx  # Single customer analysis
│   │   ├── Links.tsx        # Links management page
│   │   ├── Analysis.tsx     # Advanced analysis page
│   │   └── Reports.tsx      # Reports page
│   │
│   ├── services/            # API integration
│   │   ├── api.ts           # Base API client (axios/fetch)
│   │   ├── customers.ts     # Customer API calls
│   │   ├── links.ts         # Links API calls
│   │   ├── dashboard.ts     # Dashboard API calls
│   │   └── analysis.ts      # Analysis API calls
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── useCustomers.ts  # Customer data hook
│   │   ├── useLinks.ts      # Links data hook
│   │   ├── usePagination.ts # Pagination hook
│   │   └── useDebounce.ts   # Debounce hook for search
│   │
│   ├── store/               # State management (Zustand/Redux)
│   │   ├── customerStore.ts # Customer state
│   │   ├── filterStore.ts   # Filters state
│   │   └── uiStore.ts       # UI state (sidebar, modals)
│   │
│   ├── types/               # TypeScript types
│   │   ├── api.ts           # API response types
│   │   ├── customer.ts      # Customer types
│   │   ├── link.ts          # Link types
│   │   └── analysis.ts      # Analysis types
│   │
│   ├── utils/               # Utility functions
│   │   ├── formatters.ts    # Date, number formatting
│   │   ├── validators.ts    # Form validation
│   │   └── helpers.ts       # Generic helpers
│   │
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
│
├── public/                  # Static assets
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript config
├── vite.config.ts           # Vite config
└── tailwind.config.js       # Tailwind CSS config
```

## Technology Stack

**Required Technologies**:
- **React 18+** with TypeScript
- **Vite** for build tooling (NOT Create React App)
- **React Router v6** for routing
- **Tailwind CSS** for styling
- **Recharts** or **Chart.js** for data visualization
- **Axios** for API calls
- **Zustand** for state management (lightweight, simple)
- **React Query** (TanStack Query) for server state management
- **date-fns** for date manipulation
- **Lucide React** or **Heroicons** for icons

## TypeScript Type Definitions

Create comprehensive types matching the backend models:

```typescript
// types/api.ts
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export interface DateRangeFilter {
  from_date?: string;  // YYYY-MM format
  to_date?: string;    // YYYY-MM format
}

// types/customer.ts
export interface Customer {
  customer_id: number;
  canonical_root: string;
  brand: string;
  total_links: number;
}

export interface CustomerStats {
  customer_id: number;
  total_links: number;
  unique_publishers: number;
  date_range: {
    first_published: string;
    last_published: string;
  };
  avg_links_per_month: number;
}

// types/link.ts
export interface Link {
  id: number;
  customer_id: number;
  canonical_root: string;
  brand: string;
  pub_domain: string;
  target_url: string;
  anchor_text: string;
  published_at: string;
  inserted_at: string;
}

// types/analysis.ts
export interface GrowthData {
  month: string;
  count: number;
  cumulative: number;
}

export interface TopPublisher {
  pub_domain: string;
  link_count: number;
  percentage: number;
}

export interface TopAnchor {
  anchor_text: string;
  count: number;
}

export interface CustomerAnalysis {
  customer_id: number;
  brand: string;
  growth_data: GrowthData[];
  top_publishers: TopPublisher[];
  top_anchors: TopAnchor[];
  monthly_breakdown: Array<{
    month: string;
    count: number;
  }>;
}
```

## API Service Layer

Create clean API services with error handling:

```typescript
// services/api.ts
import axios, { AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token (future)
api.interceptors.request.use(
  (config) => {
    // Add auth token here when implemented
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle common errors
    if (error.response?.status === 404) {
      console.error('Resource not found');
    } else if (error.response?.status === 500) {
      console.error('Server error');
    }
    return Promise.reject(error);
  }
);

// services/customers.ts
import { api } from './api';
import type { PaginatedResponse, Customer, CustomerStats } from '../types';

export const customerService = {
  getAll: async (params?: PaginationParams) => {
    const { data } = await api.get<PaginatedResponse<Customer>>('/customers', { params });
    return data;
  },

  getById: async (id: number) => {
    const { data } = await api.get<Customer>(`/customers/${id}`);
    return data;
  },

  getStats: async (id: number, filters?: DateRangeFilter) => {
    const { data } = await api.get<CustomerStats>(`/customers/${id}/stats`, { params: filters });
    return data;
  },

  getLinks: async (id: number, params?: PaginationParams & DateRangeFilter) => {
    const { data } = await api.get<PaginatedResponse<Link>>(`/customers/${id}/links`, { params });
    return data;
  },

  getAnalysis: async (id: number, filters?: DateRangeFilter) => {
    const { data } = await api.get<CustomerAnalysis>(`/customers/${id}/analysis`, { params: filters });
    return data;
  },
};
```

## React Query Integration

Use React Query for efficient data fetching and caching:

```typescript
// hooks/useCustomers.ts
import { useQuery } from '@tanstack/react-query';
import { customerService } from '../services/customers';
import type { PaginationParams } from '../types';

export const useCustomers = (params?: PaginationParams) => {
  return useQuery({
    queryKey: ['customers', params],
    queryFn: () => customerService.getAll(params),
    staleTime: 5 * 60 * 1000, // 5 minutes (matches backend cache)
    retry: 2,
  });
};

export const useCustomerStats = (id: number, filters?: DateRangeFilter) => {
  return useQuery({
    queryKey: ['customer', id, 'stats', filters],
    queryFn: () => customerService.getStats(id, filters),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  });
};

export const useCustomerAnalysis = (id: number, filters?: DateRangeFilter) => {
  return useQuery({
    queryKey: ['customer', id, 'analysis', filters],
    queryFn: () => customerService.getAnalysis(id, filters),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  });
};
```

## State Management with Zustand

Use Zustand for UI state and filters:

```typescript
// store/filterStore.ts
import { create } from 'zustand';

interface FilterState {
  dateRange: {
    from_date?: string;
    to_date?: string;
  };
  searchTerm: string;
  selectedCustomer?: number;

  setDateRange: (from: string, to: string) => void;
  clearDateRange: () => void;
  setSearchTerm: (term: string) => void;
  setSelectedCustomer: (id?: number) => void;
  resetFilters: () => void;
}

export const useFilterStore = create<FilterState>((set) => ({
  dateRange: {},
  searchTerm: '',
  selectedCustomer: undefined,

  setDateRange: (from_date, to_date) => set({ dateRange: { from_date, to_date } }),
  clearDateRange: () => set({ dateRange: {} }),
  setSearchTerm: (searchTerm) => set({ searchTerm }),
  setSelectedCustomer: (selectedCustomer) => set({ selectedCustomer }),
  resetFilters: () => set({
    dateRange: {},
    searchTerm: '',
    selectedCustomer: undefined
  }),
}));
```

## Component Structure

### Dashboard Page Example

```typescript
// pages/Dashboard.tsx
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { dashboardService } from '../services/dashboard';
import { MetricCard } from '../components/dashboard/MetricCard';
import { ActivityFeed } from '../components/dashboard/ActivityFeed';
import { TopPublishers } from '../components/dashboard/TopPublishers';
import { GrowthChart } from '../components/charts/GrowthChart';

export const Dashboard: React.FC = () => {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard', 'metrics'],
    queryFn: () => dashboardService.getMetrics(),
  });

  const { data: activity } = useQuery({
    queryKey: ['dashboard', 'activity'],
    queryFn: () => dashboardService.getActivity(),
  });

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="space-y-6 p-6">
      {/* Metrics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total Customers"
          value={metrics?.total_customers}
          icon={<UsersIcon />}
        />
        <MetricCard
          title="Total Links"
          value={metrics?.total_links}
          icon={<LinkIcon />}
        />
        <MetricCard
          title="Publishers"
          value={metrics?.total_publishers}
          icon={<GlobeIcon />}
        />
        <MetricCard
          title="Domains"
          value={metrics?.total_domains}
          icon={<ServerIcon />}
        />
      </div>

      {/* Charts and Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GrowthChart />
        <TopPublishers />
      </div>

      <ActivityFeed activities={activity} />
    </div>
  );
};
```

### Customer Detail Page Example

```typescript
// pages/CustomerDetail.tsx
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useCustomerAnalysis, useCustomerStats } from '../hooks/useCustomers';
import { useFilterStore } from '../store/filterStore';
import { DateRangePicker } from '../components/common/DateRangePicker';
import { StatsCards } from '../components/customer/StatsCards';
import { GrowthChart } from '../components/charts/GrowthChart';
import { TopPublishersTable } from '../components/customer/TopPublishersTable';
import { TopAnchorsTable } from '../components/customer/TopAnchorsTable';
import { LinksTable } from '../components/customer/LinksTable';

export const CustomerDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const customerId = parseInt(id!, 10);
  const { dateRange } = useFilterStore();

  const { data: stats, isLoading: statsLoading } = useCustomerStats(
    customerId,
    dateRange
  );

  const { data: analysis, isLoading: analysisLoading } = useCustomerAnalysis(
    customerId,
    dateRange
  );

  return (
    <div className="space-y-6 p-6">
      {/* Header with filters */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">{analysis?.brand}</h1>
        <DateRangePicker />
      </div>

      {/* Stats Cards */}
      {stats && <StatsCards stats={stats} />}

      {/* Growth Chart */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Link Growth Over Time</h2>
        <GrowthChart data={analysis?.growth_data} />
      </div>

      {/* Top Publishers and Anchors */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TopPublishersTable publishers={analysis?.top_publishers} />
        <TopAnchorsTable anchors={analysis?.top_anchors} />
      </div>

      {/* Links Table */}
      <LinksTable customerId={customerId} />
    </div>
  );
};
```

## Styling Guidelines

**Use Tailwind CSS with these principles**:

1. **Color Scheme**:
   - Primary: `blue-600` for main actions
   - Success: `green-600` for positive metrics
   - Warning: `yellow-600` for alerts
   - Danger: `red-600` for errors
   - Neutral: `gray-100` to `gray-900` for backgrounds and text

2. **Typography**:
   - Headings: `font-bold text-2xl/3xl/4xl`
   - Body: `text-base text-gray-700`
   - Small text: `text-sm text-gray-500`

3. **Spacing**:
   - Use consistent spacing scale: `space-y-4`, `gap-6`, `p-6`
   - Card padding: `p-6`
   - Section gaps: `space-y-6` or `gap-6`

4. **Components**:
   - Cards: `bg-white rounded-lg shadow p-6`
   - Buttons: `px-4 py-2 rounded-md font-medium transition-colors`
   - Inputs: `border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500`

5. **Responsive Design**:
   - Mobile first approach
   - Use `md:`, `lg:`, `xl:` breakpoints
   - Grid layouts: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`

## Charts and Visualizations

**Use Recharts for data visualization**:

```typescript
// components/charts/GrowthChart.tsx
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import type { GrowthData } from '../../types';

interface GrowthChartProps {
  data?: GrowthData[];
}

export const GrowthChart: React.FC<GrowthChartProps> = ({ data }) => {
  if (!data) return null;

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="count"
          stroke="#2563eb"
          name="Monthly Links"
          strokeWidth={2}
        />
        <Line
          type="monotone"
          dataKey="cumulative"
          stroke="#10b981"
          name="Cumulative Total"
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

## Routing Structure

```typescript
// App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { Customers } from './pages/Customers';
import { CustomerDetail } from './pages/CustomerDetail';
import { Links } from './pages/Links';
import { Analysis } from './pages/Analysis';
import { Reports } from './pages/Reports';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="customers" element={<Customers />} />
            <Route path="customers/:id" element={<CustomerDetail />} />
            <Route path="links" element={<Links />} />
            <Route path="analysis" element={<Analysis />} />
            <Route path="reports" element={<Reports />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
```

## Environment Variables

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=LinkDB Analytics
VITE_APP_VERSION=2.0.0
```

## Package.json Dependencies

```json
{
  "name": "linkdb-frontend",
  "version": "2.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@tanstack/react-query": "^5.12.0",
    "axios": "^1.6.2",
    "zustand": "^4.4.7",
    "recharts": "^2.10.3",
    "date-fns": "^3.0.0",
    "lucide-react": "^0.294.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "typescript": "^5.3.3",
    "vite": "^5.0.8"
  }
}
```

## Common Components to Create

1. **Layout Components**:
   - `Layout.tsx` - Main layout with sidebar and header
   - `Sidebar.tsx` - Navigation sidebar
   - `Header.tsx` - Top header with user info
   - `Footer.tsx` - Footer component

2. **Common UI Components**:
   - `Button.tsx` - Reusable button
   - `Card.tsx` - Content card
   - `Table.tsx` - Data table with sorting/pagination
   - `Modal.tsx` - Modal dialog
   - `LoadingSpinner.tsx` - Loading indicator
   - `ErrorBoundary.tsx` - Error boundary
   - `DateRangePicker.tsx` - Date range selector
   - `SearchInput.tsx` - Search with debounce
   - `Pagination.tsx` - Pagination controls

3. **Chart Components**:
   - `LineChart.tsx` - Line chart wrapper
   - `BarChart.tsx` - Bar chart wrapper
   - `PieChart.tsx` - Pie chart wrapper
   - `AreaChart.tsx` - Area chart wrapper

4. **Dashboard Components**:
   - `MetricCard.tsx` - Metric display card
   - `ActivityFeed.tsx` - Recent activity list
   - `TopPublishers.tsx` - Top publishers widget
   - `QuickStats.tsx` - Quick stats overview

5. **Customer Components**:
   - `CustomerCard.tsx` - Customer info card
   - `CustomerList.tsx` - Customer list with search
   - `StatsCards.tsx` - Customer stats display
   - `LinksTable.tsx` - Customer links table
   - `TopPublishersTable.tsx` - Top publishers table
   - `TopAnchorsTable.tsx` - Top anchor texts table

## Error Handling

Implement comprehensive error handling:

```typescript
// components/common/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-red-600 mb-2">
              Something went wrong
            </h1>
            <p className="text-gray-600 mb-4">{this.state.error?.message}</p>
            <button
              onClick={() => this.setState({ hasError: false })}
              className="px-4 py-2 bg-blue-600 text-white rounded-md"
            >
              Try again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Performance Optimizations

1. **Code Splitting**:
   - Use `React.lazy()` for route-based code splitting
   - Split large components into smaller chunks

2. **Memoization**:
   - Use `React.memo()` for expensive components
   - Use `useMemo()` and `useCallback()` appropriately

3. **Data Fetching**:
   - React Query handles caching automatically
   - Match backend cache TTL (5 minutes)
   - Use `staleTime` and `cacheTime` appropriately

4. **Virtualization**:
   - Use `react-virtual` for large lists (>100 items)
   - Implement virtual scrolling for tables

## Accessibility

Ensure WCAG 2.1 AA compliance:

1. **Semantic HTML**: Use proper HTML5 elements
2. **ARIA Labels**: Add aria-labels where needed
3. **Keyboard Navigation**: All interactive elements focusable
4. **Color Contrast**: Minimum 4.5:1 ratio
5. **Screen Reader**: Test with screen readers

## Testing Considerations

While implementation is primary, structure code for testing:

1. **Separate Logic**: Keep business logic separate from UI
2. **Prop Types**: Use TypeScript for type safety
3. **Test IDs**: Add `data-testid` attributes for key elements
4. **Mockable Services**: API services should be easily mockable

## Export Instructions for Figma

When exporting from Figma:

1. **Component Organization**:
   - Group related components into folders
   - Use clear, descriptive names
   - Match the folder structure above

2. **Naming Conventions**:
   - Components: PascalCase (e.g., `CustomerCard`)
   - Files: PascalCase (e.g., `CustomerCard.tsx`)
   - Variables: camelCase (e.g., `customerId`)
   - Constants: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)

3. **Code Quality**:
   - Use TypeScript strict mode
   - Add proper type annotations
   - Include JSDoc comments for complex components
   - Follow ESLint and Prettier rules

4. **Responsive Design**:
   - Mobile-first approach
   - Test at breakpoints: 320px, 768px, 1024px, 1440px
   - Use Tailwind responsive utilities

5. **Assets**:
   - Export SVG icons inline or as components
   - Optimize images (WebP format preferred)
   - Use proper alt text for images

## Integration Checklist

Before merging with backend:

- [ ] All TypeScript types match backend models
- [ ] API endpoints match backend routes
- [ ] Error handling implemented
- [ ] Loading states for all async operations
- [ ] Pagination implemented correctly
- [ ] Date filtering uses YYYY-MM format
- [ ] Environment variables configured
- [ ] All components are responsive
- [ ] Accessibility standards met
- [ ] Code follows project structure
- [ ] No console errors or warnings
- [ ] Build succeeds without errors

## Development Workflow

1. **Setup**:
   ```bash
   cd gui/frontend
   npm install
   npm run dev
   ```

2. **Backend Connection**:
   - Ensure backend is running: `cd gui/backend && python app_optimized.py`
   - Backend runs on: `http://localhost:8000`
   - Frontend proxy configured in `vite.config.ts`

3. **Development**:
   - Run frontend: `npm run dev` (port 5173)
   - Backend API: `http://localhost:8000/api/v1`
   - Check CORS is configured in backend

## Final Notes

- **Priority**: Focus on Dashboard, Customers, and Customer Detail pages first
- **Backend Compatibility**: All components must work with existing API
- **No Backend Changes**: Do not modify backend code - only consume API
- **TypeScript Strict**: Use strict TypeScript for type safety
- **Performance**: Keep initial bundle size under 300KB
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge latest 2 versions)

## Questions to Address During Export

1. What specific pages from Figma should be converted?
2. Are there custom illustrations or icons to export?
3. What is the exact color palette to use?
4. Any specific animation requirements?
5. Should dark mode be implemented now or later?

---

**Export this frontend code to integrate seamlessly with the LinkDB backend. Follow the structure and patterns above for smooth integration.**
