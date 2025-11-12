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
