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

  constructor(private router: Router) {}

  login(): void {
    this.loading = true;
    this.error = '';

    // TEMP login logic (replace with backend later)
    setTimeout(() => {
      this.loading = false;

      if (this.email && this.password) {
        // ✅ CORRECT ROUTE
        this.router.navigate(['/dashboard']);
      } else {
        this.error = 'Invalid email or password';
      }
    }, 1000);
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
