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
      this.error = 'Please enter email and password';
      this.loading = false;
      return;
    }

    // Call backend API for authentication
    this.apiService.login(this.email, this.password).subscribe(
      (response: any) => {
        this.loading = false;
        
        // Debug: Log the response to see what we're getting
        console.log('Login response:', response);
        console.log('User object:', response.user);
        console.log('User role from response:', response.user?.role);
        console.log('User role from service:', this.apiService.getUserRole());
        
        // Navigate based on user role
        const role = response.user?.role || this.apiService.getUserRole();
        console.log('Final role used for routing:', role);
        
        if (role === 'admin') {
          console.log('Routing to admin dashboard');
          this.router.navigate(['/admin/dashboard']);
        } else if (role === 'department_staff' || role === 'staff') {
          console.log('Routing to staff dashboard');
          this.router.navigate(['/staff/dashboard']);
        } else {
          console.log('Routing to student dashboard');
          this.router.navigate(['/dashboard']);
        }
      },
      (error: any) => {
        this.loading = false;
        console.error('Login error:', error);
        
        if (error.status === 401) {
          this.error = 'Invalid email or password';
        } else if (error.status === 0) {
          this.error = 'Cannot connect to server. Please ensure backend is running on port 8000.';
        } else {
          this.error = error.error?.detail || 'Login failed. Please try again.';
        }
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
