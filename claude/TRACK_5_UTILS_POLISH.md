# TRACK 5: Utils, Hooks & Final Polish [5/5]

**Agent:** Full-Stack Polish Specialist
**Status:** Ready to Execute (Wait for all tracks!)
**Credits:** Part of $150 budget (Claude Code)
**Estimated Time:** 2-3 hours

---

## 🎯 Mission

Du är **Track 5** - den SISTA track i utvecklingsteamet. Din uppgift är att:
1. Skapa utilities (API client, formatters, helpers)
2. Skapa React hooks för data fetching
3. Implementera export functionality (CSV, PDF)
4. Bug fixes & polish
5. Performance optimization
6. Final testing

**VIKTIGT:** Du kör SIST! Vänta tills Track 1-4 är klara.

---

## 🚦 Boundary Rules

### ✅ DU FÅR RÖRA:
```
gui/frontend/src/utils/
├── api.js                          # API client (fetch wrapper)
├── formatters.js                   # Date, number, text formatters
├── colors.js                       # Color helpers
└── export.js                       # Export functionality

gui/frontend/src/hooks/
├── useCustomers.js                 # React Query hook för customers
├── useAnalysis.js                  # React Query hook för analysis
├── useLinks.js                     # React Query hook för links
└── useCompetitive.js               # React Query hook för competitive

gui/export/                         # Separate export service
├── export_pdf.py                   # PDF generation (Python)
└── export_csv.py                   # CSV generation (Python)
```

### ⚠️ DU FÅR OCKSÅ:
- **Refactor** any Track 2, 3, 4 code to use dina utils/hooks
- **Fix bugs** i alla tracks
- **Optimize** performance
- **Add polish** (animations, transitions, etc)

### ❌ DU FÅR INTE:
- Ändra backend API (Track 1) - bara anropa det
- Bryta functionality som redan fungerar

---

## 👥 Dependencies

| Track | Vad du behöver | Status Check |
|-------|----------------|--------------|
| **Track 1** | Backend API | `curl http://localhost:8000/health` |
| **Track 2** | Layout & common | Check components exist |
| **Track 3** | Charts | Check charts exist |
| **Track 4** | Pages | Check all routes work |

**INNAN DU BÖRJAR:**
Verifiera att ALL functionality från Track 1-4 fungerar!

---

## 📋 Din Uppgift

### Del 1: API Client (45 min)

**Fil:** `src/utils/api.js`

**Purpose:** Centralized API client med error handling, caching, loading states.

```javascript
const API_BASE_URL = 'http://localhost:8000/api';

class ApiClient {
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'API request failed');
      }

      const data = await response.json();
      return data.data || data; // Extract data from ApiResponse wrapper
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Convenience methods
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  async post(endpoint, body) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async put(endpoint, body) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }

  // Specific API methods
  async getDashboardMetrics() {
    return this.get('/dashboard/metrics');
  }

  async getCustomers() {
    return this.get('/customers');
  }

  async getCustomer(id) {
    return this.get(`/customers/${id}`);
  }

  async getCustomerAnalysis(id) {
    return this.get(`/customers/${id}/analysis`);
  }

  async getCustomerLinks(id, offset = 0, limit = 50) {
    return this.get(`/customers/${id}/links?offset=${offset}&limit=${limit}`);
  }

  async getLinks(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.get(`/links?${params}`);
  }

  async getCompetitiveOverview() {
    return this.get('/competitive/overview');
  }

  async getCompetitiveComparison(customerId) {
    return this.get(`/competitive/compare?customer_id=${customerId}`);
  }
}

export default new ApiClient();
```

### Del 2: Formatters (30 min)

**Fil:** `src/utils/formatters.js`

```javascript
// Date formatting
export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';

  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('sv-SE', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return dateString;
  }
};

export const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A';

  try {
    const date = new Date(dateString);
    return date.toLocaleString('sv-SE', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return dateString;
  }
};

// Number formatting
export const formatNumber = (num, decimals = 0) => {
  if (num === null || num === undefined) return 'N/A';

  return num.toLocaleString('sv-SE', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
};

export const formatPercent = (num, decimals = 1) => {
  if (num === null || num === undefined) return 'N/A';

  return `${num.toFixed(decimals)}%`;
};

export const formatScore = (score) => {
  if (score === null || score === undefined) return 'N/A';

  return `${score.toFixed(1)}/100`;
};

// Text formatting
export const truncate = (text, maxLength = 50) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;

  return `${text.substring(0, maxLength)}...`;
};

export const capitalize = (text) => {
  if (!text) return '';

  return text.charAt(0).toUpperCase() + text.slice(1);
};

// URL formatting
export const formatUrl = (url) => {
  if (!url) return '';

  try {
    const urlObj = new URL(url);
    return urlObj.hostname + urlObj.pathname;
  } catch {
    return url;
  }
};

// Score to status
export const getStatusFromScore = (score) => {
  if (score >= 80) return { label: 'Excellent', variant: 'success' };
  if (score >= 60) return { label: 'Good', variant: 'info' };
  if (score >= 40) return { label: 'Fair', variant: 'warning' };
  return { label: 'Poor', variant: 'danger' };
};

// Risk level formatting
export const formatRiskLevel = (risk) => {
  const riskMap = {
    high: { label: 'HIGH RISK', variant: 'danger', icon: '🚨' },
    medium: { label: 'Medium Risk', variant: 'warning', icon: '⚠️' },
    low: { label: 'Low Risk', variant: 'success', icon: '✅' },
  };

  return riskMap[risk] || riskMap.low;
};
```

### Del 3: React Query Hooks (60 min)

**Install React Query:**
```bash
cd gui/frontend
npm install @tanstack/react-query
```

**Setup Query Client** - Update `src/main.jsx`:
```jsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);
```

**Fil:** `src/hooks/useCustomers.js`

```javascript
import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

export const useCustomers = () => {
  return useQuery({
    queryKey: ['customers'],
    queryFn: () => api.getCustomers(),
  });
};

export const useCustomer = (customerId) => {
  return useQuery({
    queryKey: ['customer', customerId],
    queryFn: () => api.getCustomer(customerId),
    enabled: !!customerId,
  });
};
```

**Fil:** `src/hooks/useAnalysis.js`

```javascript
import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

export const useCustomerAnalysis = (customerId) => {
  return useQuery({
    queryKey: ['analysis', customerId],
    queryFn: () => api.getCustomerAnalysis(customerId),
    enabled: !!customerId,
    staleTime: 2 * 60 * 1000, // 2 minutes (shorter for analysis)
  });
};
```

**Fil:** `src/hooks/useLinks.js`

```javascript
import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

export const useCustomerLinks = (customerId, offset = 0, limit = 50) => {
  return useQuery({
    queryKey: ['customerLinks', customerId, offset, limit],
    queryFn: () => api.getCustomerLinks(customerId, offset, limit),
    enabled: !!customerId,
  });
};

export const useLinks = (filters = {}, offset = 0, limit = 50) => {
  return useQuery({
    queryKey: ['links', filters, offset, limit],
    queryFn: () => api.getLinks({ ...filters, offset, limit }),
  });
};
```

**Fil:** `src/hooks/useCompetitive.js`

```javascript
import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

export const useCompetitiveOverview = () => {
  return useQuery({
    queryKey: ['competitive', 'overview'],
    queryFn: () => api.getCompetitiveOverview(),
    staleTime: 10 * 60 * 1000, // 10 minutes (benchmarks change slowly)
  });
};

export const useCompetitiveComparison = (customerId) => {
  return useQuery({
    queryKey: ['competitive', 'comparison', customerId],
    queryFn: () => api.getCompetitiveComparison(customerId),
    enabled: !!customerId,
  });
};
```

### Del 4: Refactor Pages to Use Hooks (60 min)

**Refactor Track 4 pages** att använda dina hooks istället för direct fetch.

**Exempel - Dashboard.jsx:**
```jsx
import { useQuery } from '@tanstack/react-query';
import api from '../utils/api';

const Dashboard = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => api.getDashboardMetrics(),
  });

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {/* Use data här */}
    </div>
  );
};
```

**Gör samma för:**
- CustomerList.jsx
- CustomerAnalysis.jsx
- CompetitiveBenchmarking.jsx
- LinkExplorer.jsx

### Del 5: Export Functionality (45 min)

**Fil:** `src/utils/export.js`

```javascript
// Export to CSV
export const exportToCSV = (data, filename = 'export.csv') => {
  if (!data || data.length === 0) {
    alert('No data to export');
    return;
  }

  // Get headers from first object
  const headers = Object.keys(data[0]);

  // Create CSV content
  const csvContent = [
    headers.join(','),
    ...data.map(row =>
      headers.map(header => {
        const value = row[header];
        // Escape commas and quotes
        if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value;
      }).join(',')
    )
  ].join('\n');

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);

  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Export to JSON
export const exportToJSON = (data, filename = 'export.json') => {
  const jsonContent = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonContent], { type: 'application/json' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);

  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Copy to clipboard
export const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(
    () => alert('Copied to clipboard!'),
    (err) => console.error('Failed to copy:', err)
  );
};
```

**Add export buttons** till Link Explorer & Customer List.

### Del 6: Python PDF Export (Optional, 30 min)

**Fil:** `gui/export/export_pdf.py`

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import datetime

def generate_customer_report(customer_data, output_path):
    """
    Generate PDF report for a customer.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph(f"Customer Analysis Report: {customer_data['canonical_root']}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Date
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal'])
    story.append(date_text)
    story.append(Spacer(1, 24))

    # Summary Section
    summary_title = Paragraph("Executive Summary", styles['Heading1'])
    story.append(summary_title)

    summary_data = [
        ['Metric', 'Value'],
        ['Overall Score', f"{customer_data['overall_score']}/100"],
        ['Total Links', str(customer_data['total_links'])],
        ['Unique Domains', str(customer_data['unique_domains'])],
        ['Anchor Quality', f"{customer_data['anchor_quality']}/100"],
    ]

    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 24))

    # Recommendations
    rec_title = Paragraph("Top Recommendations", styles['Heading1'])
    story.append(rec_title)

    for i, rec in enumerate(customer_data.get('recommendations', [])[:5], 1):
        rec_text = Paragraph(f"{i}. {rec}", styles['Normal'])
        story.append(rec_text)
        story.append(Spacer(1, 6))

    # Build PDF
    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    # Example usage
    sample_data = {
        'canonical_root': 'bethard.com',
        'overall_score': 80.1,
        'total_links': 56,
        'unique_domains': 51,
        'anchor_quality': 59.9,
        'recommendations': [
            'Diversify anchor texts',
            'Reduce commercial keywords',
            'Maintain domain diversity',
        ]
    }

    generate_customer_report(sample_data, 'customer_report.pdf')
```

### Del 7: Bug Fixes & Polish (60 min)

**Checklist:**

- [ ] **Fix all console errors/warnings**
- [ ] **Add loading skeletons** (not just spinners)
- [ ] **Add empty states** ("No data found" messages)
- [ ] **Improve error messages** (user-friendly)
- [ ] **Add transitions/animations** (smooth page transitions)
- [ ] **Responsive fixes** (test on tablet/small screen)
- [ ] **Accessibility** (add ARIA labels, keyboard navigation)
- [ ] **Performance** (lazy load routes, optimize re-renders)

**Add Loading Skeleton Component:**
```jsx
// src/components/common/Skeleton.jsx
const Skeleton = ({ className = '', width = '100%', height = '20px' }) => {
  return (
    <div
      className={`animate-pulse bg-gray-200 rounded ${className}`}
      style={{ width, height }}
    />
  );
};

export default Skeleton;
```

**Add Empty State Component:**
```jsx
// src/components/common/EmptyState.jsx
const EmptyState = ({ message = 'No data found', icon = '📭' }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="text-6xl mb-4">{icon}</div>
      <p className="text-gray-600 text-lg">{message}</p>
    </div>
  );
};

export default EmptyState;
```

### Del 8: Performance Optimization (30 min)

**1. Lazy load routes:**
```jsx
// App.jsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const CustomerAnalysis = lazy(() => import('./pages/CustomerAnalysis'));
// ... etc

function App() {
  return (
    <Suspense fallback={<LoadingSpinner size="lg" />}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        {/* ... */}
      </Routes>
    </Suspense>
  );
}
```

**2. Memoize expensive computations:**
```jsx
import { useMemo } from 'react';

const filteredData = useMemo(() => {
  return data.filter(item => item.score > 50);
}, [data]);
```

**3. Debounce search input:**
```jsx
import { useState, useEffect } from 'react';

const useDebounce = (value, delay = 500) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
};

// Usage:
const [search, setSearch] = useState('');
const debouncedSearch = useDebounce(search);
// Use debouncedSearch for API calls
```

### Del 9: Final Testing (30 min)

**Test Everything:**

1. **Start backend:**
   ```bash
   cd gui/backend
   uvicorn app:app --reload
   ```

2. **Start frontend:**
   ```bash
   cd gui/frontend
   npm run dev
   ```

3. **Test all routes:**
   - Dashboard loads
   - Customer list works
   - Customer analysis shows all tabs
   - Charts render
   - Competitive page works
   - Link explorer works
   - Export functions work

4. **Test edge cases:**
   - Customer with no data
   - API error handling
   - Slow network (throttle in DevTools)
   - Empty search results

5. **Browser compatibility:**
   - Chrome ✓
   - Firefox ✓
   - Edge ✓

---

## 📊 Deliverables Checklist

- [ ] API client (`utils/api.js`)
- [ ] Formatters (`utils/formatters.js`)
- [ ] Export utils (`utils/export.js`)
- [ ] React Query hooks (4 files)
- [ ] Refactored pages to use hooks
- [ ] Loading skeletons
- [ ] Empty states
- [ ] Bug fixes completed
- [ ] Performance optimizations
- [ ] All tests passing
- [ ] PDF export (optional)
- [ ] Documentation updated

---

## 🎯 Success Criteria

1. **Zero console errors**
2. **All pages load fast (<2s)**
3. **Smooth interactions**
4. **Professional polish**
5. **Export works**
6. **Responsive on all screens**
7. **Accessible (keyboard nav works)**

---

## 🔄 Final Deliverable

Create: `gui/DEPLOYMENT_READY.md`

**Innehåll:**
```markdown
# LinkDB GUI - Deployment Ready

## Setup

### Backend
```bash
cd gui/backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd gui/frontend
npm install
npm run dev  # Development
npm run build  # Production
```

## Features Complete

- ✅ Dashboard with KPIs
- ✅ Customer analysis (5 tabs)
- ✅ Competitive benchmarking
- ✅ Link explorer
- ✅ Export functionality
- ✅ Responsive design
- ✅ Performance optimized

## Browser Support

- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

## Performance Metrics

- First Contentful Paint: <1s
- Time to Interactive: <2s
- Lighthouse Score: >90

## Known Issues

None!

## Future Enhancements

- Dark mode
- Advanced filters
- Real-time updates
```

---

## 🎬 Ready to Start?

1. **Wait for ALL other tracks!**
2. **Open Claude Code**
3. **Load:** `TRACK_5_UTILS_POLISH.md`
4. **Tell Claude Code:**
   ```
   Execute TRACK_5_UTILS_POLISH.md

   You are Track 5 - the FINAL track.
   Create all utilities, hooks, and export functionality.
   Refactor pages to use your hooks.
   Fix ALL bugs, optimize performance, add polish.

   This is the last step before deployment.
   Make it perfect!

   When done, create DEPLOYMENT_READY.md
   ```

**Track 5 fullbordar hela projektet!** ✨

*Estimated completion: 2-3 hours*
*Budget: ~$20-30 of $150 credits*

---

**Efter Track 5 är allt DEPLOYMENT READY!** 🚀
