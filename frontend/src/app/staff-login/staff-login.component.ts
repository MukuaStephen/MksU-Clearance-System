import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-staff-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './staff-login.component.html',
  styleUrls: ['./staff-login.component.css']
})
export class StaffLoginComponent {
  email: string = '';
  password: string = '';
  loading: boolean = false;
  error: string = '';

  constructor(private router: Router, private apiService: ApiService) {}

  login() {
    if (!this.email || !this.password) {
      this.error = 'Please enter email and password';
      return;
    }

    this.loading = true;
    this.error = '';

    this.apiService.login(this.email, this.password).subscribe(
      (response: any) => {
        this.loading = false;
        // Check if user is staff
        if (response.user.role === 'department_staff' || response.user.role === 'admin') {
          this.router.navigate(['/staff/dashboard']);
        } else {
          this.error = 'You must be a staff member to access this portal';
          this.apiService.logout().subscribe();
        }
      },
      (error: any) => {
        this.loading = false;
        if (error.status === 401) {
          this.error = 'Invalid email or password';
        } else if (error.status === 0) {
          this.error = 'Cannot connect to server. Make sure backend is running on http://localhost:8000';
        } else {
          this.error = error.error?.detail || 'Login failed. Please try again.';
        }
        console.error('Login error:', error);
      }
    );
  }

  navigateToStudent() {
    this.router.navigate(['/login']);
  }

  navigateToAdmin() {
    this.router.navigate(['/admin-login']);
  }
}
