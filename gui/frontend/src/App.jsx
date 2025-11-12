import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import CustomerList from './pages/CustomerList';
import CustomerAnalysis from './pages/CustomerAnalysis';
import CompetitiveBenchmarking from './pages/CompetitiveBenchmarking';
import LinkExplorer from './pages/LinkExplorer';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/customers" element={<CustomerList />} />
          <Route path="/customers/:id" element={<CustomerAnalysis />} />
          <Route path="/competitive" element={<CompetitiveBenchmarking />} />
          <Route path="/links" element={<LinkExplorer />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
