import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-student-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './student-login.component.html',
  styleUrls: ['./student-login.component.css']
})
export class StudentLoginComponent {

  // Login fields
  email: string = '';
  password: string = '';

  // Registration fields
  fullName: string = '';
  admissionNumber: string = '';
  passwordConfirm: string = '';

  // UI state
  isRegisterMode: boolean = false;
  loading: boolean = false;

  // Error handling
  error: string = '';

  constructor(private router: Router, private apiService: ApiService) {}

  login(): void {
    this.loading = true;
    this.error = '';

    // Validate input
    if (!this.email || !this.password) {
      this.loading = false;
      this.error = 'Please enter your email and password';
      return;
    }

    // Call backend API for authentication
    this.apiService.login(this.email, this.password).subscribe(
      (response: any) => {
        this.loading = false;
        
        // Get user role from localStorage (set by ApiService)
        const userRole = localStorage.getItem('user_role');
        
        // Route based on user role
        if (userRole === 'student') {
          this.router.navigate(['/dashboard']);
        } else if (userRole === 'department_staff') {
          this.router.navigate(['/staff/dashboard']);
        } else if (userRole === 'admin') {
          this.router.navigate(['/admin/dashboard']);
        } else {
          this.error = 'Unknown user role. Please contact support.';
        }
      },
      (error: any) => {
        this.loading = false;
        
        // Handle different error types
        if (error.status === 401) {
          this.error = 'Invalid email or password';
        } else if (error.status === 0) {
          this.error = 'Cannot connect to server. Please check your connection.';
        } else {
          this.error = error.error?.detail || error.error?.message || 'Login failed. Please try again.';
        }
        
        console.error('Login error:', error);
      }
    );
  }

  register(): void {
    this.loading = true;
    this.error = '';

    if (this.password !== this.passwordConfirm) {
      this.loading = false;
      this.error = 'Passwords do not match';
      return;
    }

    setTimeout(() => {
      this.loading = false;
      this.isRegisterMode = false;
    }, 1000);
  }

  toggleRegisterMode(): void {
    this.isRegisterMode = !this.isRegisterMode;
    this.error = '';
  }
}
