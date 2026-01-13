import API_BASE_URL from '../config/api';

// Create axios-like fetch wrapper
class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('access_token');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  getToken() {
    return this.token || localStorage.getItem('access_token');
  }

  async request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}${endpoint}`;
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers,
    };

    if (options.body && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);
      
      // Handle 401 Unauthorized - token expired
      if (response.status === 401) {
        this.setToken(null);
        window.location.href = '/login';
        throw new Error('Authentication required');
      }

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        throw {
          response: {
            status: response.status,
            data: data || { detail: response.statusText },
          },
        };
      }

      return { data };
    } catch (error) {
      throw error;
    }
  }

  get(endpoint, config = {}) {
    return this.request(endpoint, { ...config, method: 'GET' });
  }

  post(endpoint, data, config = {}) {
    return this.request(endpoint, { ...config, method: 'POST', body: data });
  }

  put(endpoint, data, config = {}) {
    return this.request(endpoint, { ...config, method: 'PUT', body: data });
  }

  patch(endpoint, data, config = {}) {
    return this.request(endpoint, { ...config, method: 'PATCH', body: data });
  }

  delete(endpoint, config = {}) {
    return this.request(endpoint, { ...config, method: 'DELETE' });
  }
}

const apiClient = new ApiClient(API_BASE_URL);

export default apiClient;
