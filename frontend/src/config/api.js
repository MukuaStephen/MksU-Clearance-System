// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// API endpoints
export const API_ENDPOINTS = {
  // Authentication
  LOGIN: `${API_BASE_URL}/auth/login/`,
  LOGOUT: `${API_BASE_URL}/auth/logout/`,
  REGISTER: `${API_BASE_URL}/auth/register/`,
  REFRESH_TOKEN: `${API_BASE_URL}/auth/token/refresh/`,
  
  // Students
  STUDENTS: `${API_BASE_URL}/students/`,
  STUDENT_ME: `${API_BASE_URL}/students/me/`,
  STUDENT_DETAIL: (id) => `${API_BASE_URL}/students/${id}/`,
  STUDENTS_ELIGIBLE: `${API_BASE_URL}/students/eligible/`,
  
  // Clearances
  CLEARANCES: `${API_BASE_URL}/clearances/`,
  CLEARANCE_DETAIL: (id) => `${API_BASE_URL}/clearances/${id}/`,
  CLEARANCE_SUBMIT: (id) => `${API_BASE_URL}/clearances/${id}/submit/`,
  
  // Approvals
  APPROVALS: `${API_BASE_URL}/approvals/`,
  APPROVAL_PROCESS: (id) => `${API_BASE_URL}/approvals/${id}/process/`,
  
  // Finance
  PAYMENTS: `${API_BASE_URL}/finance/payments/`,
  PAYMENT_DETAIL: (id) => `${API_BASE_URL}/finance/payments/${id}/`,
  PAYMENT_VERIFY: (id) => `${API_BASE_URL}/finance/payments/${id}/verify/`,
  
  // Departments
  DEPARTMENTS: `${API_BASE_URL}/departments/`,
  DEPARTMENT_DETAIL: (id) => `${API_BASE_URL}/departments/${id}/`,
  
  // Notifications
  NOTIFICATIONS: `${API_BASE_URL}/notifications/`,
  NOTIFICATION_MARK_READ: (id) => `${API_BASE_URL}/notifications/${id}/mark_read/`,
  
  // Analytics
  ANALYTICS_DASHBOARD: `${API_BASE_URL}/analytics/dashboard/`,
  ANALYTICS_CLEARANCE_COMPLETION: `${API_BASE_URL}/analytics/clearance-completion/`,
  ANALYTICS_DEPARTMENT_BOTTLENECKS: `${API_BASE_URL}/analytics/department-bottlenecks/`,
  ANALYTICS_FINANCIAL_SUMMARY: `${API_BASE_URL}/analytics/financial-summary/`,
  
  // Gown Issuance
  GOWN_ISSUANCES: `${API_BASE_URL}/gown-issuances/`,
  GOWN_ISSUANCE_DETAIL: (id) => `${API_BASE_URL}/gown-issuances/${id}/`,
  GOWN_ISSUANCE_MARK_RETURNED: (id) => `${API_BASE_URL}/gown-issuances/${id}/mark_returned/`,
  GOWN_ISSUANCES_OVERDUE: `${API_BASE_URL}/gown-issuances/overdue/`,
  GOWN_ISSUANCES_STATISTICS: `${API_BASE_URL}/gown-issuances/statistics/`,
  
  // Academics
  SCHOOLS: `${API_BASE_URL}/academics/schools/`,
  ACADEMIC_DEPARTMENTS: `${API_BASE_URL}/academics/departments/`,
  COURSES: `${API_BASE_URL}/academics/courses/`,
};

export default API_BASE_URL;
