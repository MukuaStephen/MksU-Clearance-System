import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-student-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './student-login.component.html',
  styleUrls: ['./student-login.component.css']
})
export class StudentLoginComponent {

  email: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private router: Router) {}

  login(): void {
    if (!this.email || !this.password) {
      this.errorMessage = 'Please enter email and password.';
      return;
    }

    // FRONTEND-ONLY LOGIN (simulation)
    this.errorMessage = '';
    this.router.navigate(['/dashboard']);
  }
}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-student-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './student-login.component.html',
  styleUrls: ['./student-login.component.css']
})
export class StudentLoginComponent {
  email: string = '';
  password: string = '';
  loading: boolean = false;
  error: string = '';
  isRegisterMode: boolean = false;
  
  // Registration fields
  fullName: string = '';
  admissionNumber: string = '';
  passwordConfirm: string = '';

  constructor(
    private router: Router,
    private authService: AuthService,
    private apiService: ApiService
  ) {}

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
        
        // Automatic role-based routing
        const userRole = response.user?.role || this.apiService.getUserRole();
        
        if (userRole === 'admin') {
          this.router.navigate(['/admin/dashboard']);
        } else if (userRole === 'department_staff') {
          this.router.navigate(['/staff/dashboard']);
        } else if (userRole === 'student') {
          this.router.navigate(['/dashboard']);
        } else {
          // Default to student dashboard if role is unknown
          this.router.navigate(['/dashboard']);
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

  register() {
    if (!this.email || !this.password || !this.fullName || !this.admissionNumber) {
      this.error = 'Please fill all fields';
      return;
    }

    if (this.password !== this.passwordConfirm) {
      this.error = 'Passwords do not match';
      return;
    }

    this.loading = true;
    this.error = '';

    const registerData = {
      email: this.email,
      full_name: this.fullName,
      admission_number: this.admissionNumber,
      password: this.password,
      password_confirm: this.passwordConfirm,
      role: 'student'
    };

    this.apiService.register(registerData).subscribe(
      (response: any) => {
        this.loading = false;
        // Auto-login after registration
        this.apiService.login(this.email, this.password).subscribe(
          (loginResponse: any) => {
            // Automatic role-based routing after registration
            const userRole = loginResponse.user?.role || 'student';
            
            if (userRole === 'admin') {
              this.router.navigate(['/admin/dashboard']);
            } else if (userRole === 'department_staff') {
              this.router.navigate(['/staff/dashboard']);
            } else {
              this.router.navigate(['/dashboard']);
            }
          },
          (error: any) => {
            this.error = 'Registration successful but auto-login failed. Please login manually.';
          }
        );
      },
      (error: any) => {
        this.loading = false;
        if (error.error?.email) {
          this.error = 'Email already registered';
        } else if (error.error?.admission_number) {
          this.error = 'Admission number already registered';
        } else {
          this.error = error.error?.detail || 'Registration failed. Please try again.';
        }
        console.error('Registration error:', error);
      }
    );
  }

  toggleRegisterMode() {
    this.isRegisterMode = !this.isRegisterMode;
    this.error = '';
    this.email = '';
    this.password = '';
    this.fullName = '';
    this.admissionNumber = '';
    this.passwordConfirm = '';
  }
}
