import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private apiService: ApiService, private router: Router) {}

  login(email: string, password: string, role: string) {
    return this.apiService.login(email, password).subscribe(
      (response: any) => {
        // Role-based routing
        if (role === 'student') {
          this.router.navigate(['/dashboard']);
        } else if (role === 'department_staff') {
          this.router.navigate(['/staff/dashboard']);
        } else if (role === 'admin') {
          this.router.navigate(['/admin/dashboard']);
        }
      },
      (error: any) => {
        console.error('Login error:', error);
        throw error;
      }
    );
  }

  logout() {
    return this.apiService.logout().subscribe(
      () => {
        this.router.navigate(['/login']);
      },
      (error: any) => {
        console.error('Logout error:', error);
        // Still redirect even if API call fails
        localStorage.clear();
        this.router.navigate(['/login']);
      }
    );
  }

  isAuthenticated(): boolean {
    return this.apiService.isAuthenticated();
  }

  getUserRole(): string | null {
    return this.apiService.getUserRole();
  }

  getUserId(): string | null {
    return this.apiService.getUserId();
  }

  getUserEmail(): string | null {
    return this.apiService.getUserEmail();
  }
}
