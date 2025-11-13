# Figma Export - Format & Struktur Specifikation

**VIKTIGT**: Detta dokument beskriver exakt hur koden ska exporteras från Figma för att kunna integreras direkt med backend.

## 📦 Export Format & Organisation

### Export-strategi: 6 Separata Leveranser

Exportera frontend i **6 separata zip-filer**, en för varje fas. Detta gör det enkelt att implementera och testa stegvis.

---

## 📋 Fas 0: Setup Package (EXPORT #1)

### Vad ska exporteras

**Filnamn**: `linkdb-frontend-phase0-setup.zip`

**Innehåll**:
```
linkdb-frontend-phase0-setup/
├── package.json                 # Komplett med alla dependencies
├── tsconfig.json               # TypeScript config
├── vite.config.ts              # Vite config med proxy
├── tailwind.config.js          # Tailwind config med färger
├── postcss.config.js           # PostCSS config
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore fil
├── index.html                  # HTML template
├── src/
│   ├── main.tsx                # Entry point med React Query setup
│   ├── App.tsx                 # Basic App component (placeholder)
│   └── index.css               # Global Tailwind imports
└── README.md                   # Setup instructions
```

### Exakt Package.json

```json
{
  "name": "linkdb-frontend",
  "private": true,
  "version": "2.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "@tanstack/react-query": "^5.17.0",
    "axios": "^1.6.5",
    "zustand": "^4.4.7",
    "recharts": "^2.10.3",
    "date-fns": "^3.0.6",
    "lucide-react": "^0.300.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.45",
    "@types/react-dom": "^18.2.18",
    "@types/node": "^20.10.6",
    "@typescript-eslint/eslint-plugin": "^6.16.0",
    "@typescript-eslint/parser": "^6.16.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.3",
    "vite": "^5.0.10"
  }
}
```

### Verifiering

Efter uppackning ska användaren kunna:
```bash
cd linkdb-frontend-phase0-setup
npm install
npm run dev
```

Och se en basic React app på http://localhost:5173

---

## 📋 Fas 1: Core Foundation (EXPORT #2)

### Vad ska exporteras

**Filnamn**: `linkdb-frontend-phase1-foundation.zip`

**Innehåll**:
```
linkdb-frontend-phase1-foundation/
├── src/
│   ├── types/
│   │   ├── api.ts              # API response types
│   │   ├── customer.ts         # Customer types
│   │   ├── link.ts             # Link types
│   │   ├── dashboard.ts        # Dashboard types
│   │   ├── analysis.ts         # Analysis types
│   │   └── index.ts            # Export all types
│   │
│   ├── services/
│   │   ├── api.ts              # Axios instance med interceptors
│   │   ├── customers.ts        # Customer API calls
│   │   ├── links.ts            # Links API calls
│   │   ├── dashboard.ts        # Dashboard API calls
│   │   └── analysis.ts         # Analysis API calls
│   │
│   ├── hooks/
│   │   ├── useCustomers.ts     # Customer data hooks
│   │   ├── useLinks.ts         # Links data hooks
│   │   ├── useDashboard.ts     # Dashboard data hooks
│   │   └── useDebounce.ts      # Debounce utility hook
│   │
│   └── main.tsx                # UPPDATERAD med QueryClient
│
└── INTEGRATION_TEST.md         # Guide för att testa API connection
```

### Viktiga Typer som MÅSTE matcha Backend

**`types/api.ts`**:
```typescript
// EXAKT som backend's pagination response
export interface PaginatedResponse<T> {
  items: T[];           // Lista av items
  total: number;        // Totalt antal items
  page: number;         // Nuvarande sida
  page_size: number;    // Items per sida
  total_pages: number;  // Totalt antal sidor
  has_next: boolean;    // Finns nästa sida?
  has_prev: boolean;    // Finns föregående sida?
}
```

**`types/customer.ts`**:
```typescript
// EXAKT som backend Customer model
export interface Customer {
  customer_id: number;      // Primärnyckel
  canonical_root: string;   // Domain
  brand: string;            // Brand name
  total_links: number;      // Antal backlinks
}

// EXAKT som backend CustomerStats response
export interface CustomerStats {
  customer_id: number;
  total_links: number;
  unique_publishers: number;
  date_range: {
    first_published: string;  // ISO date string
    last_published: string;   // ISO date string
  };
  avg_links_per_month?: number;
}
```

**`types/link.ts`**:
```typescript
// EXAKT som backend Link model
export interface Link {
  id: number;               // Auto-increment ID
  customer_id: number;      // Foreign key
  canonical_root: string;   // Customer domain
  brand: string;            // Customer brand
  pub_domain: string;       // Publisher domain
  target_url: string;       // Full URL to customer page
  anchor_text: string;      // Link anchor text
  published_at: string;     // ISO date: YYYY-MM-DD
  inserted_at: string;      // ISO datetime: YYYY-MM-DDTHH:MM:SS
}
```

### API Service Pattern

**ALLA API services följer samma pattern**:

```typescript
// services/[resource].ts
import api from './api';
import type { ... } from '@/types';

export const [resource]Service = {
  // GET list med pagination
  getAll: async (params?: PaginationParams) => {
    const { data } = await api.get<PaginatedResponse<Resource>>(
      '/[resources]',
      { params }
    );
    return data;
  },

  // GET single by ID
  getById: async (id: number) => {
    const { data } = await api.get<Resource>(`/[resources]/${id}`);
    return data;
  },

  // GET with filters
  getFiltered: async (filters?: FilterParams) => {
    const { data } = await api.get<PaginatedResponse<Resource>>(
      '/[resources]',
      { params: filters }
    );
    return data;
  },
};
```

### React Query Hook Pattern

**ALLA hooks följer samma pattern**:

```typescript
// hooks/use[Resource].ts
import { useQuery } from '@tanstack/react-query';
import { [resource]Service } from '@/services/[resource]';

export const use[Resources] = (params?: PaginationParams) => {
  return useQuery({
    queryKey: ['[resources]', params],  // Cache key
    queryFn: () => [resource]Service.getAll(params),
    staleTime: 5 * 60 * 1000,  // 5 min (matchar backend cache)
    retry: 1,
  });
};

export const use[Resource] = (id: number) => {
  return useQuery({
    queryKey: ['[resource]', id],
    queryFn: () => [resource]Service.getById(id),
    enabled: !!id && id > 0,  // Kör bara om ID finns
    staleTime: 5 * 60 * 1000,
  });
};
```

### Verifiering

Test-komponent för att verifiera backend connection:

**`src/App.tsx`** (temporary test):
```typescript
import { useDashboardMetrics } from './hooks/useDashboard';

function App() {
  const { data, isLoading, error } = useDashboardMetrics();

  if (isLoading) return <div className="p-8">Laddar...</div>;
  if (error) return <div className="p-8 text-red-600">Error: {String(error)}</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Backend Test ✅</h1>
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
```

Om detta fungerar → Backend integration OK! ✅

---

## 📋 Fas 2: Common Components (EXPORT #3)

### Vad ska exporteras

**Filnamn**: `linkdb-frontend-phase2-components.zip`

**Innehåll**:
```
linkdb-frontend-phase2-components/
└── src/
    └── components/
        └── common/
            ├── index.ts              # Export all components
            ├── Button.tsx            # Button med variants
            ├── Card.tsx              # Content card
            ├── LoadingSpinner.tsx    # Loading state
            ├── EmptyState.tsx        # Empty state display
            ├── Table.tsx             # Generic data table
            ├── Pagination.tsx        # Pagination controls
            ├── SearchInput.tsx       # Search med debounce
            └── ErrorBoundary.tsx     # Error boundary
```

### Komponent Interface Standard

**ALLA komponenter ska följa detta pattern**:

1. **TypeScript Props Interface**:
```typescript
interface [Component]Props {
  // Required props (utan ?)
  requiredProp: string;

  // Optional props (med ?)
  optionalProp?: string;

  // Children (om applicable)
  children?: React.ReactNode;

  // Styling
  className?: string;

  // Event handlers
  onClick?: () => void;
}
```

2. **Export Pattern**:
```typescript
export const [Component]: React.FC<[Component]Props> = ({ ... }) => {
  // Component logic
  return ( ... );
};
```

3. **Tailwind Classes**:
   - Använd `clsx()` för conditional classes
   - Alla colors ska använda Tailwind color scale
   - Spacing: använd 4px grid (p-4, gap-6, etc.)

### Table Component - Speciell

**Table.tsx MÅSTE vara generic**:

```typescript
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

export function Table<T>({ ... }: TableProps<T>) { ... }
```

**Används så här**:
```typescript
<Table
  data={customers}
  columns={[
    { key: 'id', header: 'ID', render: (c) => c.customer_id },
    { key: 'brand', header: 'Brand', render: (c) => c.brand },
  ]}
  keyExtractor={(c) => c.customer_id}
/>
```

### Verifiering

Test alla komponenter i Storybook-stil:

**`src/App.tsx`** (temporary):
```typescript
import { Button, Card, Table, Pagination } from './components/common';

// Test alla komponenter tillsammans
```

---

## 📋 Fas 3: Layout & Navigation (EXPORT #4)

### Vad ska exporteras

**Filnamn**: `linkdb-frontend-phase3-layout.zip`

**Innehåll**:
```
linkdb-frontend-phase3-layout/
├── src/
│   ├── components/
│   │   └── layout/
│   │       ├── Layout.tsx       # Main layout wrapper
│   │       ├── Sidebar.tsx      # Navigation sidebar
│   │       ├── Header.tsx       # Top header
│   │       └── index.ts         # Exports
│   │
│   └── App.tsx                  # UPPDATERAD med React Router
│
└── ROUTES.md                    # Route specification
```

### Router Struktur - EXAKT

**`App.tsx`** MÅSTE ha denna structure:

```typescript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';

// Pages (placeholders initially)
const Dashboard = () => <div>Dashboard</div>;
const Customers = () => <div>Customers</div>;
const CustomerDetail = () => <div>Customer Detail</div>;
const Links = () => <div>Links</div>;
const Analysis = () => <div>Analysis</div>;
const Reports = () => <div>Reports</div>;
const NotFound = () => <div>404</div>;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* Redirect root to dashboard */}
          <Route index element={<Navigate to="/dashboard" replace />} />

          {/* Main routes */}
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="customers" element={<Customers />} />
          <Route path="customers/:id" element={<CustomerDetail />} />
          <Route path="links" element={<Links />} />
          <Route path="analysis" element={<Analysis />} />
          <Route path="reports" element={<Reports />} />

          {/* 404 */}
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### Navigation Items - EXAKT

**Sidebar navigation MÅSTE ha dessa items i denna ordning**:

```typescript
const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Customers', href: '/customers', icon: Users },
  { name: 'Links', href: '/links', icon: Link },
  { name: 'Analysis', href: '/analysis', icon: BarChart3 },
  { name: 'Reports', href: '/reports', icon: FileText },
];
```

### Layout Dimensions - EXAKT

- **Sidebar width**: `w-64` (256px)
- **Header height**: `h-16` (64px)
- **Content max-width**: `max-w-7xl` (1280px)
- **Content padding**: `px-4 sm:px-6 lg:px-8`

---

## 📋 Fas 4: Dashboard Page (EXPORT #5)

### Vad ska exporteras

**Filnamn**: `linkdb-frontend-phase4-dashboard.zip`

**Innehåll**:
```
linkdb-frontend-phase4-dashboard/
└── src/
    ├── components/
    │   └── dashboard/
    │       ├── MetricCard.tsx         # Metric display card
    │       ├── ActivityFeed.tsx       # Recent activity
    │       ├── TopPublishers.tsx      # Top publishers widget
    │       └── index.ts               # Exports
    │
    └── pages/
        └── Dashboard.tsx              # Complete dashboard page
```

### Dashboard Page Structure - EXAKT

**Layout grid MÅSTE vara**:

```typescript
<div className="space-y-6">
  {/* Header */}
  <div>
    <h1 className="text-2xl font-bold">Dashboard</h1>
    <p className="text-sm text-gray-500">Overview...</p>
  </div>

  {/* Metrics - 4 cards */}
  <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
    <MetricCard title="Total Customers" value={metrics?.total_customers} icon={Users} />
    <MetricCard title="Total Links" value={metrics?.total_links} icon={Link} />
    <MetricCard title="Publishers" value={metrics?.total_publishers} icon={Globe} />
    <MetricCard title="Domains" value={metrics?.total_domains} icon={Server} />
  </div>

  {/* Widgets - 2 columns */}
  <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
    <TopPublishers publishers={publishers} />
    <ActivityFeed activities={activity} />
  </div>
</div>
```

### Data Flow - EXAKT

```typescript
// 1. Fetch data med hooks
const { data: metrics } = useDashboardMetrics();
const { data: activity } = useDashboardActivity();
const { data: publishers } = useTopPublishers();

// 2. Pass till components
<MetricCard value={metrics?.total_customers} />
<ActivityFeed activities={activity} />
<TopPublishers publishers={publishers} />

// 3. Components renderar data
// Använd optional chaining (?) för att hantera undefined
// Visa loading state medan data fetchas
```

---

## 📋 Fas 5: Customers Pages (EXPORT #6)

### Vad ska exporteras

**Filnamn**: `linkdb-frontend-phase5-customers.zip`

**Innehåll**:
```
linkdb-frontend-phase5-customers/
├── src/
│   ├── components/
│   │   └── customer/
│   │       ├── StatsCards.tsx         # Customer stats display
│   │       ├── TopPublishersTable.tsx # Top publishers table
│   │       ├── TopAnchorsTable.tsx    # Top anchors table
│   │       ├── LinksTable.tsx         # Customer links table
│   │       └── index.ts               # Exports
│   │
│   ├── pages/
│   │   ├── Customers.tsx              # Customers list page
│   │   └── CustomerDetail.tsx         # Single customer page
│   │
│   └── types/
│       └── analysis.ts                # UPPDATERAD med analysis types
│
└── CUSTOMER_FLOW.md                   # User flow documentation
```

### Customer List Page - Features

**MÅSTE ha dessa features i denna ordning**:

1. **Header** med title och description
2. **SearchInput** för att filtrera customers
3. **Table** med customers data
4. **Columns**:
   - ID (customer_id)
   - Brand (brand + canonical_root)
   - Total Links (total_links)
   - Actions (View Details button)
5. **Pagination** om fler än 20 customers

### Customer Detail Page - Structure

**MÅSTE ha dessa sektioner i denna ordning**:

1. **Header**
   - Customer brand name som h1
   - Customer ID som subtitle
   - (Future: Date range filter)

2. **Stats Cards** (3 cards i rad)
   - Total Links (med Link icon)
   - Publishers (med Globe icon)
   - Date Range (med Calendar icon)

3. **Analytics Grid** (2 columns på desktop)
   - **Left**: Top Publishers Table (top 10)
   - **Right**: Top Anchors Table (top 10)

4. **(Future)**: Growth Chart
5. **(Future)**: Links Table med filtering

### URL Pattern - EXAKT

```
/customers                    → Lista alla customers
/customers/:id                → Visa customer med ID
/customers/117                → Example: customer 117
/customers/117/links          → (Future) Customer links
```

### Data Dependencies

**CustomerDetail page MÅSTE fetcha**:

```typescript
const { id } = useParams<{ id: string }>();
const customerId = parseInt(id!, 10);

// 1. Customer stats
const { data: stats } = useCustomerStats(customerId);

// 2. Customer analysis
const { data: analysis } = useCustomerAnalysis(customerId);
```

**Båda requests körs parallellt automatiskt av React Query!**

---

## 🔄 Integration Checklist för Varje Fas

Efter varje fas export, verifiera:

### ✅ TypeScript Types
- [ ] Alla types matchar backend models EXAKT
- [ ] Inga `any` types
- [ ] Optional fields markerade med `?`
- [ ] All data från backend har types

### ✅ API Integration
- [ ] Service methods anropar rätt endpoints
- [ ] Query parameters skickas korrekt
- [ ] Response types matchar PaginatedResponse<T> där applicable
- [ ] Error handling finns

### ✅ React Query
- [ ] QueryKeys är unika och inkluderar params
- [ ] staleTime satt till 5 * 60 * 1000 (5 min)
- [ ] enabled property används för conditional queries
- [ ] Loading och error states hanteras

### ✅ Components
- [ ] Props har TypeScript interfaces
- [ ] Components är reusable (ej hardcoded data)
- [ ] Tailwind classes används (ej inline styles)
- [ ] clsx() används för conditional classes
- [ ] Responsive design (grid-cols-1 md:grid-cols-2 lg:grid-cols-4)

### ✅ Styling
- [ ] Färger från Tailwind palette
- [ ] primary-600 för huvudfärg
- [ ] Spacing consistent (gap-6, space-y-6, p-6)
- [ ] Text sizes consistent
- [ ] Hover states finns
- [ ] Focus states finns (för accessibility)

### ✅ Performance
- [ ] Inga onödiga re-renders
- [ ] Ingen data fetching i loops
- [ ] Images optimerade (om några)
- [ ] Kod splitting används (lazy loading för pages)

---

## 📤 Export Checklist

För VARJE fas export, inkludera:

### 📄 Fil-struktur
```
[phase-name]/
├── src/                    # Source files
├── package.json            # (Fas 0 only)
├── README.md              # Installation/usage instructions
└── INTEGRATION.md         # Backend integration notes
```

### 📝 README.md Template

```markdown
# LinkDB Frontend - [Fas Namn]

## Installation

\`\`\`bash
# Om Fas 0: Från scratch
npm install

# Om Fas 1-6: Copy till existing projekt
cp -r src/* /path/to/existing/src/
\`\`\`

## Vad ingår

- Lista alla komponenter/filer
- Vad varje fil gör
- Dependencies (om nya)

## Integration

1. Kopiera filer till rätt platser
2. Verifiera imports
3. Testa funktionalitet
4. Kör type-check: \`npm run type-check\`

## Backend Dependencies

- Endpoint: [lista endpoints]
- Response format: [beskriv]
- Required types: [lista]

## Verifiering

[Steg för att verifiera att det fungerar]
\`\`\`bash
npm run dev
# Navigate to [URL]
# Förväntat resultat: [beskriv]
\`\`\`
```

---

## 🎯 Export Summary

### Varje Export Ska Innehålla:

1. **Källkod**
   - Alla `.ts` och `.tsx` filer
   - Korrekt folder struktur
   - `index.ts` exports där applicable

2. **Dokumentation**
   - README.md med instruktioner
   - INTEGRATION.md med backend notes
   - Inline comments för komplex logik

3. **TypeScript**
   - Alla types definierade
   - Inga errors vid `tsc --noEmit`
   - Strikta types (ej `any`)

4. **Testbarhet**
   - Komponenter kan testas isolerat
   - Props interfaces väl definierade
   - Mock data examples i docs

### Filnamns-konvention

```
linkdb-frontend-phase[0-6]-[name].zip
```

Examples:
- `linkdb-frontend-phase0-setup.zip`
- `linkdb-frontend-phase1-foundation.zip`
- `linkdb-frontend-phase2-components.zip`
- `linkdb-frontend-phase3-layout.zip`
- `linkdb-frontend-phase4-dashboard.zip`
- `linkdb-frontend-phase5-customers.zip`

---

## 🚀 Implementation Order

**Detta är viktigt!** Implementera i EXAKT denna ordning:

1. **Fas 0** - Setup → Verify: `npm run dev` fungerar
2. **Fas 1** - Foundation → Verify: API connection fungerar
3. **Fas 2** - Components → Verify: Komponenter renderas
4. **Fas 3** - Layout → Verify: Navigation fungerar
5. **Fas 4** - Dashboard → Verify: Data från backend visas
6. **Fas 5** - Customers → Verify: Full CRUD flow fungerar

**Gå INTE vidare till nästa fas förrän föregående är verifierad!**

---

## ❌ Vanliga Fel att Undvika

### 1. Type Mismatches
```typescript
// ❌ FEL - Matchar ej backend
interface Customer {
  id: number;        // Backend använder customer_id
  name: string;      // Backend använder brand
}

// ✅ RÄTT - Matchar backend exakt
interface Customer {
  customer_id: number;
  brand: string;
  canonical_root: string;
  total_links: number;
}
```

### 2. Endpoint Paths
```typescript
// ❌ FEL - Fel endpoint
api.get('/customer/${id}')     // Singular
api.get('/api/customers/${id}') // /api/ inkluderad (finns i baseURL)

// ✅ RÄTT
api.get(`/customers/${id}`)     // Plural, no /api/
```

### 3. Date Formats
```typescript
// ❌ FEL - Fel format
from_date: '2024/01/01'        // Använder /
from_date: '2024-01-01'        // Full date (backend vill YYYY-MM)

// ✅ RÄTT
from_date: '2024-01'           // YYYY-MM format
```

### 4. Pagination
```typescript
// ❌ FEL - Fel struktur
{ data: Customer[], count: number }

// ✅ RÄTT - Matchar backend
{
  items: Customer[],
  total: number,
  page: number,
  page_size: number,
  total_pages: number,
  has_next: boolean,
  has_prev: boolean
}
```

---

## 🎨 Figma Export Instruktioner

När du exporterar från Figma:

1. **Organisera layers** enligt folder structure
2. **Namnge components** med PascalCase
3. **Använd Auto Layout** för spacing
4. **Definiera Tailwind classes** i kommentarer
5. **Gruppera** relaterade components
6. **Exportera** en fas i taget
7. **Verifiera** struktur innan nästa fas

### Exempel på Figma Organisation

```
Figma File
├── 📁 Phase 0 - Setup
│   └── Config files (copy från spec)
│
├── 📁 Phase 1 - Foundation
│   ├── Types
│   ├── Services
│   └── Hooks
│
├── 📁 Phase 2 - Components
│   ├── Button
│   ├── Card
│   ├── Table
│   └── ...
│
└── ...
```

---

**Med denna specifikation kan du exportera korrekt formaterad kod som integrerar direkt med backend!** 🎉
