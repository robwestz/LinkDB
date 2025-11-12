import { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import LoadingSpinner from './components/common/LoadingSpinner';

// Lazy load pages for better performance
const Dashboard = lazy(() => import('./pages/Dashboard'));
const CustomerList = lazy(() => import('./pages/CustomerList'));
const CustomerAnalysis = lazy(() => import('./pages/CustomerAnalysis'));
const CompetitiveBenchmarking = lazy(() => import('./pages/CompetitiveBenchmarking'));
const LinkExplorer = lazy(() => import('./pages/LinkExplorer'));
const AIChat = lazy(() => import('./pages/AIChat'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Router>
      <Layout>
        <Suspense fallback={
          <div className="flex items-center justify-center h-64">
            <LoadingSpinner size="lg" />
          </div>
        }>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<CustomerList />} />
            <Route path="/customers/:id" element={<CustomerAnalysis />} />
            <Route path="/competitive" element={<CompetitiveBenchmarking />} />
            <Route path="/links" element={<LinkExplorer />} />
            <Route path="/ai-chat" element={<AIChat />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Suspense>
      </Layout>
    </Router>
  );
}

export default App;
