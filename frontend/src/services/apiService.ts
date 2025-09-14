import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface QueryRequest {
  query: string;
  include_chart: boolean;
}

export interface QueryResponse {
  query: string;
  response: string;
  chart_generated: boolean;
  chart_url?: string;
  execution_time: number;
  timestamp: string;
  status: string;
}

export interface UserProfile {
  id: number;
  firstname: string;
  lastname: string;
  username: string;
  city: string;
  state: string;
  country: string;
  weight: number;
  profile: string;
  profile_medium: string;
  follower_count: number;
  friend_count: number;
  date_preference: string;
  measurement_preference: string;
}

export interface UserStats {
  summary: {
    total_runs: number;
    total_miles: number;
    total_time_minutes: number;
    total_elevation: number;
    this_year_miles: number;
  };
  averages: {
    avg_pace: number;
    avg_distance: number;
    avg_time: number;
    avg_heartrate: number;
  };
  bests: {
    fastest_pace: number;
    longest_run: number;
    longest_time: number;
  };
  weekly_stats: any[];
  monthly_stats: any[];
  day_of_week_stats: any[];
}

export interface DataOverview {
  total_activities: number;
  date_range: {
    start: string;
    end: string;
  };
  activity_types: { [key: string]: number };
  columns: string[];
  sample_data: any[];
  data_loaded_at: string;
}

export interface ExampleQueries {
  examples: Array<{
    category: string;
    queries: string[];
  }>;
}

export interface RateLimitStatus {
  query_count: number;
  remaining_queries: number;
  max_queries: number;
  session_start: string | null;
  rate_limited: boolean;
}

class ApiService {
  private getAuthHeaders() {
    const token = localStorage.getItem('strava_access_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  // Health check
  async getHealth() {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  }

  // Authentication
  async exchangeCodeForToken(code: string) {
    const response = await axios.post(`${API_BASE_URL}/auth/token`, { code });
    return response.data;
  }

  // Data refresh
  async refreshData() {
    const response = await axios.post(`${API_BASE_URL}/data/refresh`, {}, {
      headers: this.getAuthHeaders(),
    });
    return response.data;
  }

  // Data status
  async getDataStatus() {
    const response = await axios.get(`${API_BASE_URL}/data/status`);
    return response.data;
  }

  // User profile
  async getUserProfile() {
    try {
      const response = await axios.get(`${API_BASE_URL}/user/profile`, {
        headers: this.getAuthHeaders(),
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 401) {
        // Token is invalid or expired
        localStorage.removeItem('strava_access_token');
        throw new Error('Authentication failed. Please log in again.');
      }
      throw error;
    }
  }

  // User stats
  async getUserStats() {
    const response = await axios.get(`${API_BASE_URL}/user/stats`, {
      headers: this.getAuthHeaders(),
    });
    return response.data;
  }

  // Recent activities
  async getRecentActivities(limit: number = 10) {
    const response = await axios.get(`${API_BASE_URL}/user/recent-activities?limit=${limit}`, {
      headers: this.getAuthHeaders(),
    });
    return response.data;
  }

  // Process query
  async processQuery(request: QueryRequest): Promise<QueryResponse> {
    const response = await axios.post(`${API_BASE_URL}/query`, request, {
      headers: this.getAuthHeaders(),
    });
    return response.data;
  }

  // Get chart
  async getChart(): Promise<Blob> {
    const response = await axios.get(`${API_BASE_URL}/chart`, {
      responseType: 'blob',
    });
    return response.data;
  }

  // Get chart URL
  getChartUrl(): string {
    return `${API_BASE_URL}/chart?t=${Date.now()}`;
  }

  // Get data overview
  async getDataOverview(): Promise<DataOverview> {
    const response = await axios.get(`${API_BASE_URL}/data/overview`);
    return response.data;
  }

  // Get example queries
  async getExampleQueries(): Promise<ExampleQueries> {
    const response = await axios.get(`${API_BASE_URL}/examples`);
    return response.data;
  }

  // Get rate limit status
  async getRateLimitStatus(): Promise<RateLimitStatus> {
    const response = await axios.get(`${API_BASE_URL}/rate-limit`, {
      headers: this.getAuthHeaders(),
    });
    return response.data;
  }
}

export const apiService = new ApiService();