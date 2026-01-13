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

  // 🔐 Login fields
  email = '';
  password = '';

  // 📝 Registration fields
  fullName = '';
  admissionNumber = '';
  passwordConfirm = '';

  // 🔄 UI state
  isRegisterMode = false;
  loading = false;

  // ❌ Error handling
  error = '';

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
        if (userRole === 'admin') {
          this.router.navigate(['/admin/dashboard']);
        } else if (userRole === 'department_staff') {
          this.router.navigate(['/staff/dashboard']);
        } else if (userRole === 'student') {
          this.router.navigate(['/dashboard']);
        } else {
          this.error = 'Unknown user role. Please contact support.';
        }
      },
      (error: any) => {
        this.loading = false;
        
        // Handle different error types with user-friendly messages
        if (error.status === 401 || error.status === 400) {
          this.error = 'Wrong email or password. Please try again.';
        } else if (error.status === 0) {
          this.error = 'Cannot connect to server. Please check your connection.';
        } else if (error.name === 'TimeoutError') {
          this.error = 'Request timed out. Please try again.';
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

    if (!this.fullName || !this.email || !this.admissionNumber || !this.password) {
      this.loading = false;
      this.error = 'Please fill in all fields';
      return;
    }

    const registrationData = {
      email: this.email,
      password: this.password,
      password_confirm: this.passwordConfirm,
      full_name: this.fullName,
      admission_number: this.admissionNumber,
      role: 'student'
    };

    // Call backend API for registration
    this.apiService.register(registrationData).subscribe(
      (response: any) => {
        this.loading = false;
        // Registration successful, navigate to dashboard
        this.router.navigate(['/dashboard']);
      },
      (error: any) => {
        this.loading = false;
        console.error('Registration error:', error);
        
        if (error.status === 0) {
          this.error = 'Cannot connect to server. Please ensure backend is running.';
        } else if (error.error?.email) {
          this.error = 'Email already exists';
        } else if (error.error?.admission_number) {
          this.error = 'Admission number already exists';
        } else {
          this.error = error.error?.detail || 'Registration failed. Please try again.';
        }
      }
    );
  }

  toggleRegisterMode(): void {
    this.isRegisterMode = !this.isRegisterMode;
    this.error = '';
  }
}
