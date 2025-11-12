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
