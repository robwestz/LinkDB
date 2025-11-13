# LinkDB Frontend - Stegvis Implementationsguide

Denna guide beskriver hur frontend ska byggas i 6 faser för att säkerställa smidig integration med backend.

## 📋 Översikt

**Total estimerad tid**: 6-8 timmar uppdelat på 6 faser
**Strategi**: Bottom-up approach - bygg grunden först, sedan sidorna
**Verifiering**: Efter varje fas - testa integration med backend

---

## Fas 0: Setup & Grundkonfiguration (30 min)

### Mål
Sätt upp projektet och verifiera att allt fungerar innan vi börjar bygga komponenter.

### Steg för Steg

#### 1. Skapa projektet
```bash
cd gui/
npm create vite@latest frontend -- --template react-ts
cd frontend
```

#### 2. Installera dependencies
```bash
npm install react-router-dom @tanstack/react-query axios zustand
npm install recharts date-fns lucide-react clsx
npm install -D tailwindcss postcss autoprefixer
npm install -D @types/node
npx tailwindcss init -p
```

#### 3. Konfigurera Tailwind CSS

**tailwind.config.js**:
```javascript
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
          500: '#3b82f6',
          600: '#2563eb',  // Main primary color
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
}
```

**src/index.css**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}
```

#### 4. Konfigurera Vite

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

#### 5. Konfigurera TypeScript

**tsconfig.json** (lägg till i compilerOptions):
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

#### 6. Skapa mappstruktur
```bash
mkdir -p src/{components,pages,services,hooks,store,types,utils}
mkdir -p src/components/{common,layout,charts,dashboard,customer}
```

#### 7. Skapa .env fil

**`.env`**:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=LinkDB Analytics
```

### Verifiering Fas 0

- [ ] `npm run dev` startar utan errors
- [ ] Kan öppna http://localhost:5173
- [ ] Tailwind CSS fungerar (testa en klass)
- [ ] Mappstrukturen är skapad
- [ ] TypeScript kompilerar utan errors

**Test**: Ändra något i App.tsx med Tailwind klasser och verifiera hot reload.

---

## Fas 1: Core Foundation (1 tim)

### Mål
Bygg grundläggande infrastruktur: types, API client, och basic state management.

### Vad ska skapas

#### 1. TypeScript Types

**`src/types/api.ts`**:
```typescript
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
  from_date?: string;  // YYYY-MM
  to_date?: string;    // YYYY-MM
}

export interface ApiError {
  detail: string;
  status: number;
}
```

**`src/types/customer.ts`**:
```typescript
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
  avg_links_per_month?: number;
}
```

**`src/types/link.ts`**:
```typescript
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
```

**`src/types/dashboard.ts`**:
```typescript
export interface DashboardMetrics {
  total_customers: number;
  total_links: number;
  total_publishers: number;
  total_domains: number;
}

export interface Activity {
  id: number;
  customer_id: number;
  brand: string;
  pub_domain: string;
  published_at: string;
  anchor_text: string;
}

export interface TopPublisher {
  pub_domain: string;
  link_count: number;
}
```

**`src/types/index.ts`**:
```typescript
export * from './api';
export * from './customer';
export * from './link';
export * from './dashboard';
```

#### 2. API Client

**`src/services/api.ts`**:
```typescript
import axios, { AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('Network Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
```

#### 3. Basic Services

**`src/services/customers.ts`**:
```typescript
import api from './api';
import type {
  PaginatedResponse,
  Customer,
  CustomerStats,
  PaginationParams,
  DateRangeFilter
} from '@/types';

export const customerService = {
  getAll: async (params?: PaginationParams) => {
    const { data } = await api.get<PaginatedResponse<Customer>>('/customers', { params });
    return data;
  },

  getStats: async (id: number, filters?: DateRangeFilter) => {
    const { data } = await api.get<CustomerStats>(`/customers/${id}/stats`, { params: filters });
    return data;
  },
};
```

**`src/services/dashboard.ts`**:
```typescript
import api from './api';
import type { DashboardMetrics, Activity, TopPublisher } from '@/types';

export const dashboardService = {
  getMetrics: async () => {
    const { data } = await api.get<DashboardMetrics>('/dashboard/metrics');
    return data;
  },

  getActivity: async (limit = 10) => {
    const { data } = await api.get<Activity[]>('/dashboard/activity', {
      params: { limit },
    });
    return data;
  },

  getTopPublishers: async (limit = 10) => {
    const { data } = await api.get<TopPublisher[]>('/dashboard/top-publishers', {
      params: { limit },
    });
    return data;
  },
};
```

#### 4. React Query Setup

**`src/main.tsx`**:
```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes (matches backend cache)
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
)
```

#### 5. Basic Hooks

**`src/hooks/useCustomers.ts`**:
```typescript
import { useQuery } from '@tanstack/react-query';
import { customerService } from '@/services/customers';
import type { PaginationParams } from '@/types';

export const useCustomers = (params?: PaginationParams) => {
  return useQuery({
    queryKey: ['customers', params],
    queryFn: () => customerService.getAll(params),
  });
};

export const useCustomerStats = (id: number) => {
  return useQuery({
    queryKey: ['customer', id, 'stats'],
    queryFn: () => customerService.getStats(id),
    enabled: !!id && id > 0,
  });
};
```

**`src/hooks/useDashboard.ts`**:
```typescript
import { useQuery } from '@tanstack/react-query';
import { dashboardService } from '@/services/dashboard';

export const useDashboardMetrics = () => {
  return useQuery({
    queryKey: ['dashboard', 'metrics'],
    queryFn: () => dashboardService.getMetrics(),
  });
};

export const useDashboardActivity = () => {
  return useQuery({
    queryKey: ['dashboard', 'activity'],
    queryFn: () => dashboardService.getActivity(),
  });
};

export const useTopPublishers = () => {
  return useQuery({
    queryKey: ['dashboard', 'top-publishers'],
    queryFn: () => dashboardService.getTopPublishers(),
  });
};
```

### Verifiering Fas 1

**Skapa en test-komponent** för att verifiera API integration:

**`src/App.tsx`**:
```typescript
import { useDashboardMetrics } from './hooks/useDashboard';

function App() {
  const { data, isLoading, error } = useDashboardMetrics();

  if (isLoading) return <div className="p-8">Loading...</div>;
  if (error) return <div className="p-8 text-red-600">Error: {String(error)}</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Backend Connection Test</h1>
      {data && (
        <div className="space-y-2">
          <p>Total Customers: {data.total_customers}</p>
          <p>Total Links: {data.total_links}</p>
          <p>Total Publishers: {data.total_publishers}</p>
        </div>
      )}
    </div>
  );
}

export default App;
```

**Verifieringschecklist**:
- [ ] Backend körs på port 8000
- [ ] `npm run dev` startar utan errors
- [ ] Data visas från backend i browsern
- [ ] Inga TypeScript errors
- [ ] Inga console errors i browser
- [ ] Hot reload fungerar

**Om det inte fungerar**:
1. Verifiera att backend körs: `curl http://localhost:8000/api/v1/dashboard/metrics`
2. Kolla Network tab i DevTools
3. Verifiera CORS settings i backend (ska vara konfigurerat från tidigare)

---

## Fas 2: Common Components (1.5 tim)

### Mål
Bygg återanvändbara UI-komponenter som används överallt.

### Vad ska skapas

#### 1. Button Component

**`src/components/common/Button.tsx`**:
```typescript
import React from 'react';
import { Loader2 } from 'lucide-react';
import clsx from 'clsx';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  className,
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
    outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={clsx(
        baseStyles,
        variants[variant],
        sizes[size],
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
      {children}
    </button>
  );
};
```

#### 2. Card Component

**`src/components/common/Card.tsx`**:
```typescript
import React from 'react';
import clsx from 'clsx';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  padding = 'md'
}) => {
  const paddingStyles = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <div className={clsx(
      'bg-white rounded-lg shadow',
      paddingStyles[padding],
      className
    )}>
      {children}
    </div>
  );
};
```

#### 3. Loading Spinner

**`src/components/common/LoadingSpinner.tsx`**:
```typescript
import React from 'react';
import { Loader2 } from 'lucide-react';
import clsx from 'clsx';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  className
}) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className={clsx('flex items-center justify-center', className)}>
      <Loader2 className={clsx(sizes[size], 'animate-spin text-primary-600')} />
    </div>
  );
};
```

#### 4. Empty State

**`src/components/common/EmptyState.tsx`**:
```typescript
import React from 'react';
import { LucideIcon } from 'lucide-react';

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  action,
}) => {
  return (
    <div className="text-center py-12">
      {Icon && (
        <Icon className="mx-auto h-12 w-12 text-gray-400" />
      )}
      <h3 className="mt-2 text-sm font-medium text-gray-900">{title}</h3>
      {description && (
        <p className="mt-1 text-sm text-gray-500">{description}</p>
      )}
      {action && (
        <div className="mt-6">
          {action}
        </div>
      )}
    </div>
  );
};
```

#### 5. Table Component

**`src/components/common/Table.tsx`**:
```typescript
import React from 'react';
import clsx from 'clsx';

interface Column<T> {
  key: string;
  header: string;
  render: (item: T) => React.ReactNode;
  className?: string;
}

interface TableProps<T> {
  data: T[];
  columns: Column<T>[];
  keyExtractor: (item: T) => string | number;
  isLoading?: boolean;
  emptyMessage?: string;
}

export function Table<T>({
  data,
  columns,
  keyExtractor,
  isLoading,
  emptyMessage = 'No data available',
}: TableProps<T>) {
  if (isLoading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  if (data.length === 0) {
    return <div className="text-center py-8 text-gray-500">{emptyMessage}</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                className={clsx(
                  'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
                  column.className
                )}
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((item) => (
            <tr key={keyExtractor(item)} className="hover:bg-gray-50">
              {columns.map((column) => (
                <td
                  key={column.key}
                  className={clsx(
                    'px-6 py-4 whitespace-nowrap text-sm',
                    column.className
                  )}
                >
                  {column.render(item)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

#### 6. Pagination Component

**`src/components/common/Pagination.tsx`**:
```typescript
import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './Button';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  hasNext: boolean;
  hasPrev: boolean;
}

export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  hasNext,
  hasPrev,
}) => {
  return (
    <div className="flex items-center justify-between px-4 py-3 sm:px-6">
      <div className="flex justify-between sm:hidden">
        <Button
          variant="outline"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={!hasPrev}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={!hasNext}
        >
          Next
        </Button>
      </div>
      <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div>
          <p className="text-sm text-gray-700">
            Page <span className="font-medium">{currentPage}</span> of{' '}
            <span className="font-medium">{totalPages}</span>
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={!hasPrev}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={!hasNext}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
};
```

#### 7. Export Components

**`src/components/common/index.ts`**:
```typescript
export { Button } from './Button';
export { Card } from './Card';
export { LoadingSpinner } from './LoadingSpinner';
export { EmptyState } from './EmptyState';
export { Table } from './Table';
export { Pagination } from './Pagination';
```

### Verifiering Fas 2

**Skapa test page** för komponenter:

**`src/App.tsx`**:
```typescript
import { Button, Card, LoadingSpinner, Table } from './components/common';
import { useCustomers } from './hooks/useCustomers';

function App() {
  const { data, isLoading } = useCustomers({ page: 1, page_size: 5 });

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold">Component Test</h1>

      {/* Button Test */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">Buttons</h2>
        <div className="flex gap-4">
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button isLoading>Loading</Button>
        </div>
      </Card>

      {/* Table Test */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">Customers Table</h2>
        {isLoading ? (
          <LoadingSpinner />
        ) : data ? (
          <Table
            data={data.items}
            columns={[
              { key: 'id', header: 'ID', render: (c) => c.customer_id },
              { key: 'brand', header: 'Brand', render: (c) => c.brand },
              { key: 'domain', header: 'Domain', render: (c) => c.canonical_root },
              { key: 'links', header: 'Links', render: (c) => c.total_links },
            ]}
            keyExtractor={(c) => c.customer_id}
          />
        ) : null}
      </Card>
    </div>
  );
}

export default App;
```

**Verifieringschecklist**:
- [ ] Alla buttons renderas korrekt
- [ ] Cards har korrekt styling
- [ ] Table visar data från backend
- [ ] LoadingSpinner spinner
- [ ] Inga TypeScript errors
- [ ] Inga console errors

---

## Fas 3: Layout & Navigation (1 tim)

### Mål
Bygg huvudlayout med sidebar navigation och header.

### Vad ska skapas

#### 1. Layout Component

**`src/components/layout/Layout.tsx`**:
```typescript
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

export const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Header />
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};
```

#### 2. Sidebar Component

**`src/components/layout/Sidebar.tsx`**:
```typescript
import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Users,
  Link as LinkIcon,
  BarChart3,
  FileText,
} from 'lucide-react';
import clsx from 'clsx';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Customers', href: '/customers', icon: Users },
  { name: 'Links', href: '/links', icon: LinkIcon },
  { name: 'Analysis', href: '/analysis', icon: BarChart3 },
  { name: 'Reports', href: '/reports', icon: FileText },
];

export const Sidebar: React.FC = () => {
  return (
    <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-64 lg:flex-col">
      <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6 pb-4">
        <div className="flex h-16 shrink-0 items-center">
          <h1 className="text-2xl font-bold text-primary-600">
            LinkDB
          </h1>
        </div>
        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigation.map((item) => (
                  <li key={item.name}>
                    <NavLink
                      to={item.href}
                      className={({ isActive }) =>
                        clsx(
                          isActive
                            ? 'bg-primary-50 text-primary-600'
                            : 'text-gray-700 hover:bg-gray-50 hover:text-primary-600',
                          'group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6'
                        )
                      }
                    >
                      {({ isActive }) => (
                        <>
                          <item.icon
                            className={clsx(
                              isActive
                                ? 'text-primary-600'
                                : 'text-gray-400 group-hover:text-primary-600',
                              'h-6 w-6 shrink-0'
                            )}
                          />
                          {item.name}
                        </>
                      )}
                    </NavLink>
                  </li>
                ))}
              </ul>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};
```

#### 3. Header Component

**`src/components/layout/Header.tsx`**:
```typescript
import React from 'react';
import { Menu } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
      <button
        type="button"
        className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
      >
        <Menu className="h-6 w-6" />
      </button>

      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div className="flex flex-1"></div>
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          <div className="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-200" />
          <div className="text-sm font-medium text-gray-700">
            Admin User
          </div>
        </div>
      </div>
    </div>
  );
};
```

#### 4. Setup Router

**`src/App.tsx`**:
```typescript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';

// Placeholder pages
const Dashboard = () => <div className="text-2xl">Dashboard Page</div>;
const Customers = () => <div className="text-2xl">Customers Page</div>;
const Links = () => <div className="text-2xl">Links Page</div>;
const Analysis = () => <div className="text-2xl">Analysis Page</div>;
const Reports = () => <div className="text-2xl">Reports Page</div>;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="customers" element={<Customers />} />
          <Route path="links" element={<Links />} />
          <Route path="analysis" element={<Analysis />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

### Verifiering Fas 3

**Verifieringschecklist**:
- [ ] Sidebar visas på vänster sida
- [ ] Navigation links fungerar (URL ändras)
- [ ] Active state visas korrekt på navigation
- [ ] Header är sticky (scroll och se)
- [ ] Layout är responsiv (testa mindre skärm)
- [ ] Placeholder pages renderas

**Test**: Klicka runt mellan sidorna och verifiera routing.

---

## Fas 4: Dashboard Page (1.5 tim)

### Mål
Bygg komplett Dashboard-sida med metrics, charts och activity.

### Vad ska skapas

#### 1. Metric Card Component

**`src/components/dashboard/MetricCard.tsx`**:
```typescript
import React from 'react';
import { LucideIcon } from 'lucide-react';
import { Card } from '../common/Card';

interface MetricCardProps {
  title: string;
  value: number | string | undefined;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  icon: Icon,
  trend,
}) => {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="mt-2 text-3xl font-semibold text-gray-900">
            {value?.toLocaleString() ?? '-'}
          </p>
          {trend && (
            <p className={`mt-2 text-sm ${trend.isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
            </p>
          )}
        </div>
        <div className="rounded-full bg-primary-100 p-3">
          <Icon className="h-6 w-6 text-primary-600" />
        </div>
      </div>
    </Card>
  );
};
```

#### 2. Activity Feed

**`src/components/dashboard/ActivityFeed.tsx`**:
```typescript
import React from 'react';
import { formatDistanceToNow } from 'date-fns';
import { Card } from '../common/Card';
import { EmptyState } from '../common/EmptyState';
import { Clock } from 'lucide-react';
import type { Activity } from '@/types';

interface ActivityFeedProps {
  activities?: Activity[];
  isLoading?: boolean;
}

export const ActivityFeed: React.FC<ActivityFeedProps> = ({
  activities,
  isLoading,
}) => {
  if (isLoading) {
    return <Card><div className="text-center py-8">Loading...</div></Card>;
  }

  if (!activities || activities.length === 0) {
    return (
      <Card>
        <EmptyState
          icon={Clock}
          title="No recent activity"
          description="New links will appear here"
        />
      </Card>
    );
  }

  return (
    <Card>
      <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
      <div className="space-y-4">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-start gap-4 border-b pb-4 last:border-0">
            <div className="flex-1">
              <p className="font-medium text-gray-900">{activity.brand}</p>
              <p className="text-sm text-gray-600 truncate">{activity.anchor_text}</p>
              <p className="text-xs text-gray-500 mt-1">{activity.pub_domain}</p>
            </div>
            <div className="text-xs text-gray-500">
              {formatDistanceToNow(new Date(activity.published_at), { addSuffix: true })}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
```

#### 3. Top Publishers Widget

**`src/components/dashboard/TopPublishers.tsx`**:
```typescript
import React from 'react';
import { Card } from '../common/Card';
import type { TopPublisher } from '@/types';

interface TopPublishersProps {
  publishers?: TopPublisher[];
  isLoading?: boolean;
}

export const TopPublishers: React.FC<TopPublishersProps> = ({
  publishers,
  isLoading,
}) => {
  if (isLoading) {
    return <Card><div className="text-center py-8">Loading...</div></Card>;
  }

  return (
    <Card>
      <h2 className="text-lg font-semibold mb-4">Top Publishers</h2>
      <div className="space-y-3">
        {publishers?.map((publisher, index) => (
          <div key={publisher.pub_domain} className="flex items-center gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-sm font-semibold text-primary-600">
              {index + 1}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {publisher.pub_domain}
              </p>
              <p className="text-xs text-gray-500">
                {publisher.link_count} links
              </p>
            </div>
            <div className="flex-shrink-0">
              <div className="w-24 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full"
                  style={{
                    width: `${Math.min((publisher.link_count / (publishers[0]?.link_count ?? 1)) * 100, 100)}%`,
                  }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
```

#### 4. Dashboard Page

**`src/pages/Dashboard.tsx`**:
```typescript
import React from 'react';
import { Users, Link, Globe, Server } from 'lucide-react';
import { useDashboardMetrics, useDashboardActivity, useTopPublishers } from '@/hooks/useDashboard';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { ActivityFeed } from '@/components/dashboard/ActivityFeed';
import { TopPublishers } from '@/components/dashboard/TopPublishers';
import { LoadingSpinner } from '@/components/common';

export const Dashboard: React.FC = () => {
  const { data: metrics, isLoading: metricsLoading } = useDashboardMetrics();
  const { data: activity, isLoading: activityLoading } = useDashboardActivity();
  const { data: publishers, isLoading: publishersLoading } = useTopPublishers();

  if (metricsLoading) {
    return <LoadingSpinner className="py-12" />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your link building performance
        </p>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Total Customers"
          value={metrics?.total_customers}
          icon={Users}
        />
        <MetricCard
          title="Total Links"
          value={metrics?.total_links}
          icon={Link}
        />
        <MetricCard
          title="Publishers"
          value={metrics?.total_publishers}
          icon={Globe}
        />
        <MetricCard
          title="Domains"
          value={metrics?.total_domains}
          icon={Server}
        />
      </div>

      {/* Charts and Publishers */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <TopPublishers publishers={publishers} isLoading={publishersLoading} />
        <ActivityFeed activities={activity} isLoading={activityLoading} />
      </div>
    </div>
  );
};
```

#### 5. Update Router

**`src/App.tsx`** - Uppdatera importen:
```typescript
import { Dashboard } from './pages/Dashboard';
// ... rest stays the same
```

### Verifiering Fas 4

**Verifieringschecklist**:
- [ ] Dashboard visar 4 metric cards med data från backend
- [ ] Top Publishers widget visar data
- [ ] Activity Feed visar senaste aktiviteter
- [ ] Allt laddar utan errors
- [ ] Data är formatted korrekt (numbers med tusentalsavgränsare)
- [ ] Responsive layout fungerar

**Test**:
1. Öppna http://localhost:5173/dashboard
2. Verifiera att alla siffror stämmer med backend data
3. Testa responsive (minimera fönster)

---

## Fas 5: Customers Page (1.5 tim)

### Mål
Bygg Customers-sida med lista, sökning och detaljvy.

### Vad ska skapas

#### 1. Search Input Component

**`src/components/common/SearchInput.tsx`**:
```typescript
import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';

interface SearchInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  debounceMs?: number;
}

export const SearchInput: React.FC<SearchInputProps> = ({
  value,
  onChange,
  placeholder = 'Search...',
  debounceMs = 300,
}) => {
  const [localValue, setLocalValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      onChange(localValue);
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [localValue, debounceMs, onChange]);

  return (
    <div className="relative">
      <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
        <Search className="h-5 w-5 text-gray-400" />
      </div>
      <input
        type="text"
        className="block w-full rounded-md border-0 py-2 pl-10 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
        placeholder={placeholder}
        value={localValue}
        onChange={(e) => setLocalValue(e.target.value)}
      />
    </div>
  );
};
```

#### 2. Customers Page

**`src/pages/Customers.tsx`**:
```typescript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCustomers } from '@/hooks/useCustomers';
import { Card, Table, Pagination, SearchInput, LoadingSpinner } from '@/components/common';
import { ExternalLink } from 'lucide-react';

export const Customers: React.FC = () => {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');

  const { data, isLoading } = useCustomers({
    page,
    page_size: 20,
  });

  const filteredData = data?.items.filter((customer) =>
    searchTerm === '' ||
    customer.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.canonical_root.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return <LoadingSpinner className="py-12" />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Customers</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage and analyze your customers
          </p>
        </div>
      </div>

      <Card>
        <div className="mb-4">
          <SearchInput
            value={searchTerm}
            onChange={setSearchTerm}
            placeholder="Search customers..."
          />
        </div>

        <Table
          data={filteredData ?? []}
          columns={[
            {
              key: 'id',
              header: 'ID',
              render: (customer) => (
                <span className="font-medium">{customer.customer_id}</span>
              ),
            },
            {
              key: 'brand',
              header: 'Brand',
              render: (customer) => (
                <div>
                  <div className="font-medium text-gray-900">{customer.brand}</div>
                  <div className="text-sm text-gray-500">{customer.canonical_root}</div>
                </div>
              ),
            },
            {
              key: 'links',
              header: 'Total Links',
              render: (customer) => (
                <span className="text-gray-900">{customer.total_links}</span>
              ),
            },
            {
              key: 'actions',
              header: '',
              render: (customer) => (
                <button
                  onClick={() => navigate(`/customers/${customer.customer_id}`)}
                  className="text-primary-600 hover:text-primary-900 flex items-center gap-1"
                >
                  View Details
                  <ExternalLink className="h-4 w-4" />
                </button>
              ),
            },
          ]}
          keyExtractor={(customer) => customer.customer_id}
          isLoading={isLoading}
          emptyMessage="No customers found"
        />

        {data && data.total_pages > 1 && (
          <div className="mt-4">
            <Pagination
              currentPage={data.page}
              totalPages={data.total_pages}
              onPageChange={setPage}
              hasNext={data.has_next}
              hasPrev={data.has_prev}
            />
          </div>
        )}
      </Card>
    </div>
  );
};
```

#### 3. Customer Detail - Types först

**`src/types/analysis.ts`**:
```typescript
export interface GrowthData {
  month: string;
  count: number;
  cumulative?: number;
}

export interface TopPublisher {
  pub_domain: string;
  link_count: number;
  percentage?: number;
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
  monthly_breakdown?: Array<{
    month: string;
    count: number;
  }>;
}
```

#### 4. Customer Analysis Service & Hook

**`src/services/customers.ts`** - Lägg till:
```typescript
import type { CustomerAnalysis } from '@/types/analysis';

// Add to customerService object:
export const customerService = {
  // ... existing methods ...

  getAnalysis: async (id: number, filters?: DateRangeFilter) => {
    const { data } = await api.get<CustomerAnalysis>(
      `/customers/${id}/analysis`,
      { params: filters }
    );
    return data;
  },
};
```

**`src/hooks/useCustomers.ts`** - Lägg till:
```typescript
export const useCustomerAnalysis = (id: number, filters?: DateRangeFilter) => {
  return useQuery({
    queryKey: ['customer', id, 'analysis', filters],
    queryFn: () => customerService.getAnalysis(id, filters),
    enabled: !!id && id > 0,
  });
};
```

#### 5. Customer Detail Page

**`src/pages/CustomerDetail.tsx`**:
```typescript
import React from 'react';
import { useParams } from 'react-router-dom';
import { useCustomerStats, useCustomerAnalysis } from '@/hooks/useCustomers';
import { Card, LoadingSpinner } from '@/components/common';
import { Link, Globe, Calendar } from 'lucide-react';
import { format } from 'date-fns';

export const CustomerDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const customerId = parseInt(id!, 10);

  const { data: stats, isLoading: statsLoading } = useCustomerStats(customerId);
  const { data: analysis, isLoading: analysisLoading } = useCustomerAnalysis(customerId);

  if (statsLoading || analysisLoading) {
    return <LoadingSpinner className="py-12" />;
  }

  if (!stats || !analysis) {
    return <div className="text-center py-12">Customer not found</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{analysis.brand}</h1>
        <p className="mt-1 text-sm text-gray-500">
          Customer ID: {customerId}
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        <Card>
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-primary-100 p-3">
              <Link className="h-6 w-6 text-primary-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Links</p>
              <p className="text-2xl font-semibold">{stats.total_links}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-green-100 p-3">
              <Globe className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Publishers</p>
              <p className="text-2xl font-semibold">{stats.unique_publishers}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-blue-100 p-3">
              <Calendar className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Date Range</p>
              <p className="text-sm font-medium">
                {stats.date_range.first_published &&
                  format(new Date(stats.date_range.first_published), 'MMM yyyy')}
                {' - '}
                {stats.date_range.last_published &&
                  format(new Date(stats.date_range.last_published), 'MMM yyyy')}
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Top Publishers */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <h2 className="text-lg font-semibold mb-4">Top Publishers</h2>
          <div className="space-y-3">
            {analysis.top_publishers.slice(0, 10).map((publisher, index) => (
              <div key={publisher.pub_domain} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                  <span className="text-sm text-gray-900">{publisher.pub_domain}</span>
                </div>
                <span className="text-sm font-medium">{publisher.link_count} links</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Top Anchors */}
        <Card>
          <h2 className="text-lg font-semibold mb-4">Top Anchor Texts</h2>
          <div className="space-y-3">
            {analysis.top_anchors.slice(0, 10).map((anchor, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                  <span className="text-sm text-gray-900 truncate">{anchor.anchor_text}</span>
                </div>
                <span className="text-sm font-medium ml-4">{anchor.count}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
```

#### 6. Update Router

**`src/App.tsx`** - Lägg till:
```typescript
import { Customers } from './pages/Customers';
import { CustomerDetail } from './pages/CustomerDetail';

// In Routes:
<Route path="customers" element={<Customers />} />
<Route path="customers/:id" element={<CustomerDetail />} />
```

### Verifiering Fas 5

**Verifieringschecklist**:
- [ ] Customers lista visar alla kunder med data
- [ ] Sökning filtrerar kunder korrekt
- [ ] Pagination fungerar
- [ ] Click på "View Details" går till detail page
- [ ] Customer detail visar stats cards
- [ ] Top Publishers och Top Anchors visas
- [ ] Alla data från backend visas korrekt

**Test**:
1. Gå till /customers
2. Sök efter en kund
3. Klicka "View Details"
4. Verifiera all data stämmer

---

## Fas 6: Final Polish & Production (1 tim)

### Mål
Fixa de sista detaljerna, error handling, och production build.

### Vad ska göras

#### 1. Error Boundary

**`src/components/common/ErrorBoundary.tsx`**:
```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';
import { Button } from './Button';

interface Props {
  children: ReactNode;
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
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <AlertTriangle className="mx-auto h-12 w-12 text-red-500 mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Something went wrong
            </h1>
            <p className="text-gray-600 mb-4">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <Button
              onClick={() => window.location.reload()}
              variant="primary"
            >
              Reload Page
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

#### 2. Update Main with ErrorBoundary

**`src/main.tsx`**:
```typescript
import { ErrorBoundary } from './components/common/ErrorBoundary';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    </ErrorBoundary>
  </React.StrictMode>,
)
```

#### 3. Add 404 Page

**`src/pages/NotFound.tsx`**:
```typescript
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Home } from 'lucide-react';
import { Button } from '@/components/common';

export const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-9xl font-bold text-primary-600">404</h1>
        <p className="mt-4 text-2xl font-semibold text-gray-900">Page not found</p>
        <p className="mt-2 text-gray-600">
          The page you're looking for doesn't exist.
        </p>
        <Button
          onClick={() => navigate('/dashboard')}
          variant="primary"
          className="mt-6"
        >
          <Home className="h-5 w-5 mr-2" />
          Go to Dashboard
        </Button>
      </div>
    </div>
  );
};
```

**Update Router** i `App.tsx`:
```typescript
import { NotFound } from './pages/NotFound';

// Add as last route:
<Route path="*" element={<NotFound />} />
```

#### 4. Production Build Setup

**Update `package.json` scripts**:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit"
  }
}
```

#### 5. README för frontend

**`gui/frontend/README.md`**:
```markdown
# LinkDB Frontend

React + TypeScript frontend for LinkDB Analytics.

## Tech Stack

- React 18
- TypeScript
- Vite
- React Router v6
- TanStack Query (React Query)
- Tailwind CSS
- Recharts
- Axios
- Zustand
- date-fns
- Lucide React

## Getting Started

### Prerequisites

- Node.js 18+
- Backend running on http://localhost:8000

### Installation

\`\`\`bash
npm install
\`\`\`

### Development

\`\`\`bash
npm run dev
\`\`\`

Open http://localhost:5173

### Build

\`\`\`bash
npm run build
\`\`\`

### Preview Production Build

\`\`\`bash
npm run preview
\`\`\`

## Environment Variables

Create a `.env` file:

\`\`\`env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=LinkDB Analytics
\`\`\`

## Project Structure

\`\`\`
src/
├── components/
│   ├── common/         # Reusable UI components
│   ├── layout/         # Layout components
│   ├── dashboard/      # Dashboard specific
│   └── customer/       # Customer specific
├── pages/             # Page components
├── services/          # API services
├── hooks/             # Custom hooks
├── types/             # TypeScript types
└── utils/             # Utilities
\`\`\`

## Backend Integration

This frontend integrates with the FastAPI backend at `gui/backend/`.

API Base: `http://localhost:8000/api/v1`

All TypeScript types match backend Pydantic models.
```

### Verifiering Fas 6

**Final Checklist**:

**Functionality:**
- [ ] All pages load without errors
- [ ] Navigation works correctly
- [ ] Data loads from backend
- [ ] Search and filtering work
- [ ] Pagination works
- [ ] Error states show correctly
- [ ] 404 page works

**Performance:**
- [ ] Initial load < 3 seconds
- [ ] No unnecessary re-renders
- [ ] Images/assets optimized

**Build:**
- [ ] `npm run build` succeeds
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Build size reasonable (<500KB main chunk)

**Integration:**
- [ ] Backend connection works
- [ ] All API endpoints respond
- [ ] CORS configured correctly
- [ ] Data formats match

**Testing:**
```bash
# Type check
npm run type-check

# Build
npm run build

# Preview
npm run preview
```

---

## 🎯 Sammanfattning: Körplan

### Dag 1 (4 timmar)
1. **Fas 0**: Setup (30 min) ✅
2. **Fas 1**: Foundation (1 tim) ✅
3. **Fas 2**: Components (1.5 tim) ✅
4. **Fas 3**: Layout (1 tim) ✅

**Checkpoint**: Har du en fungerande app med layout och basic components? Kan du navigera mellan sidor?

### Dag 2 (4 timmar)
5. **Fas 4**: Dashboard (1.5 tim) ✅
6. **Fas 5**: Customers (1.5 tim) ✅
7. **Fas 6**: Polish (1 tim) ✅

**Final Check**: Production build fungerar och allt integrerar med backend!

---

## 🚀 Nästa Steg Efter Fas 6

När allt ovan är klart kan du fortsätta med:

1. **Links Page** - Lista alla links med advanced filtering
2. **Analysis Page** - Advanced analytics med charts
3. **Reports Page** - Generate and export reports
4. **Dark Mode** - Implementera dark mode toggle
5. **Mobile Menu** - Förbättra mobile navigation
6. **Advanced Charts** - Recharts implementation för growth data

---

## 💡 Tips

- **Commit ofta**: Efter varje fas, commit dina ändringar
- **Testa löpande**: Verifiera varje fas innan du går vidare
- **Backend först**: Håll backend körandes under hela processen
- **DevTools**: Använd React DevTools och Network tab för debugging
- **Hot reload**: Vite's hot reload är din vän - se ändringar direkt

## ❓ Troubleshooting

**"Cannot GET /api/..."**
- Verifiera att backend körs
- Kolla proxy settings i vite.config.ts

**"CORS Error"**
- Kolla CORS settings i backend config.py
- Verifiera ALLOWED_ORIGINS inkluderar http://localhost:5173

**TypeScript errors**
- `npm run type-check` för att se alla errors
- Fixa types i types/ mappen först

**Build fails**
- Kör `npm run type-check` först
- Fixa alla TypeScript errors
- Kolla att alla imports är korrekta

---

**Lycka till! Du har nu en komplett guide för att bygga frontend steg för steg! 🎉**
