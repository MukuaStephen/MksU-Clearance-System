import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap, timeout } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api';
  private authTokenSubject = new BehaviorSubject<string | null>(this.getToken());
  public authToken$ = this.authTokenSubject.asObservable();

  constructor(private http: HttpClient) {}

  // ============ Authentication ============
  register(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/register/`, data);
  }

  login(email: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/login/`, { email, password }).pipe(
      timeout(10000), // 10 second timeout
      tap((response: any) => {
        // Backend returns tokens under response.tokens { access, refresh }
        const tokens = response?.tokens || {};
        const access = tokens.access;
        const refresh = tokens.refresh;

        if (access) {
          localStorage.setItem('access_token', access);
          if (refresh) {
            localStorage.setItem('refresh_token', refresh);
          }
          if (response.user) {
            localStorage.setItem('user_role', response.user.role);
            localStorage.setItem('user_id', response.user.id);
            localStorage.setItem('user_email', response.user.email);
          }
          this.authTokenSubject.next(access);
        }
      })
    );
  }

  logout(): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/logout/`, {}).pipe(
      tap(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_role');
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_email');
        this.authTokenSubject.next(null);
      })
    );
  }

  refreshToken(): Observable<any> {
    const refresh = localStorage.getItem('refresh_token');
    return this.http.post(`${this.baseUrl}/auth/token/refresh/`, { refresh }).pipe(
      tap((response: any) => {
        if (response.access) {
          localStorage.setItem('access_token', response.access);
          this.authTokenSubject.next(response.access);
        }
      })
    );
  }

  verifyToken(token: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/verify/`, { token });
  }

  getProfile(): Observable<any> {
    return this.http.get(`${this.baseUrl}/auth/profile/`, { headers: this.getHeaders() });
  }

  changePassword(oldPassword: string, newPassword: string): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/auth/change-password/`,
      { old_password: oldPassword, new_password: newPassword },
      { headers: this.getHeaders() }
    );
  }

  // ============ Students ============
  getStudents(): Observable<any> {
    return this.http.get(`${this.baseUrl}/students/`, { headers: this.getHeaders() });
  }

  getStudent(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/students/${id}/`, { headers: this.getHeaders() });
  }

  createStudent(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/students/`, data, { headers: this.getHeaders() });
  }

  updateStudent(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/students/${id}/`, data, { headers: this.getHeaders() });
  }

  deleteStudent(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/students/${id}/`, { headers: this.getHeaders() });
  }

  // ============ Clearances ============
  getClearances(filters?: any): Observable<any> {
    let url = `${this.baseUrl}/clearances/`;
    if (filters) {
      const params = new URLSearchParams();
      Object.keys(filters).forEach(key => {
        if (filters[key]) {
          params.append(key, filters[key]);
        }
      });
      if (params.toString()) {
        url += `?${params.toString()}`;
      }
    }
    return this.http.get(url, { headers: this.getHeaders() });
  }

  getClearance(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/clearances/${id}/`, { headers: this.getHeaders() });
  }

  createClearance(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/clearances/`, data, { headers: this.getHeaders() });
  }

  updateClearance(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/clearances/${id}/`, data, { headers: this.getHeaders() });
  }

  deleteClearance(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/clearances/${id}/`, { headers: this.getHeaders() });
  }

  getClearanceStatus(studentId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/students/${studentId}/clearance-status/`, {
      headers: this.getHeaders()
    });
  }

  // ============ Approvals (Staff) ============
  getApprovals(filters?: any): Observable<any> {
    let url = `${this.baseUrl}/approvals/`;
    if (filters) {
      const params = new URLSearchParams();
      Object.keys(filters).forEach(key => {
        if (filters[key]) {
          params.append(key, filters[key]);
        }
      });
      if (params.toString()) {
        url += `?${params.toString()}`;
      }
    }
    return this.http.get(url, { headers: this.getHeaders() });
  }

  getApproval(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/approvals/${id}/`, { headers: this.getHeaders() });
  }

  createApproval(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/approvals/`, data, { headers: this.getHeaders() });
  }

  updateApproval(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/approvals/${id}/`, data, { headers: this.getHeaders() });
  }

  approveApproval(id: number, data?: any): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/approvals/${id}/approve/`,
      data || {},
      { headers: this.getHeaders() }
    );
  }

  rejectApproval(id: number, data?: any): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/approvals/${id}/reject/`,
      data || {},
      { headers: this.getHeaders() }
    );
  }

  // ============ Departments ============
  getDepartments(): Observable<any> {
    return this.http.get(`${this.baseUrl}/departments/`, { headers: this.getHeaders() });
  }

  getDepartment(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/departments/${id}/`, { headers: this.getHeaders() });
  }

  // ============ Notifications ============
  getNotifications(): Observable<any> {
    return this.http.get(`${this.baseUrl}/notifications/`, { headers: this.getHeaders() });
  }

  markNotificationAsRead(id: number): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/notifications/${id}/mark-as-read/`,
      {},
      { headers: this.getHeaders() }
    );
  }

  // ============ Finance ============
  getPayments(): Observable<any> {
    return this.http.get(`${this.baseUrl}/finance/payments/`, { headers: this.getHeaders() });
  }

  getInvoices(): Observable<any> {
    return this.http.get(`${this.baseUrl}/finance/invoices/`, { headers: this.getHeaders() });
  }

  // ============ Helper Methods ============
  private getHeaders(): HttpHeaders {
    const token = this.getToken();
    if (token) {
      return new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      });
    }
    return new HttpHeaders({
      'Content-Type': 'application/json'
    });
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getUserRole(): string | null {
    return localStorage.getItem('user_role');
  }

  getUserId(): string | null {
    return localStorage.getItem('user_id');
  }

  getUserEmail(): string | null {
    return localStorage.getItem('user_email');
  }
}
