import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { StudentClearanceComponent } from '../student-clearance/student-clearance.component';
import { ClearanceService } from '../services/clearance.service';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-student-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    StudentClearanceComponent
  ],
  templateUrl: './student-dashboard.component.html',
  styleUrls: ['./student-dashboard.component.css']
})
export class StudentDashboardComponent implements OnInit {

  // controls content area
  activeView: 'dashboard' | 'clearance' | 'profile' = 'dashboard';

  // profile/password
  oldPassword = '';
  newPassword = '';
  passwordMessage = '';
  userEmail = '';
  userName = '';

  constructor(
    public clearanceService: ClearanceService,
    private router: Router,
    private apiService: ApiService
  ) {}

  ngOnInit() {
    // Check authentication
    if (!this.apiService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }

    // Load user profile
    this.userEmail = this.apiService.getUserEmail() || '';
    this.loadProfile();
  }

  loadProfile() {
    this.apiService.getProfile().subscribe(
      (response: any) => {
        this.userName = response.full_name || response.email;
      },
      (error: any) => {
        console.error('Error loading profile:', error);
      }
    );
  }

  // ===== SIDEBAR ACTIONS =====
  showDashboard(): void {
    this.activeView = 'dashboard';
  }

  showClearance(): void {
    this.activeView = 'clearance';
  }

  showProfile(): void {
    this.activeView = 'profile';
    this.passwordMessage = '';
  }

  logout(): void {
    this.apiService.logout().subscribe(
      () => {
        this.router.navigate(['/login']);
      },
      (error: any) => {
        // Clear local storage and redirect even if logout fails
        localStorage.clear();
        this.router.navigate(['/login']);
      }
    );
  }

  changePassword(): void {
    if (!this.oldPassword || !this.newPassword) {
      this.passwordMessage = 'Please fill in both password fields.';
      return;
    }

    // Call backend API to change password
    this.apiService.changePassword(this.oldPassword, this.newPassword).subscribe(
      (response: any) => {
        this.passwordMessage = 'Password changed successfully.';
        this.oldPassword = '';
        this.newPassword = '';
      },
      (error: any) => {
        console.error('Password change error:', error);
        if (error.error?.old_password) {
          this.passwordMessage = 'Current password is incorrect.';
        } else {
          this.passwordMessage = 'Failed to change password. Please try again.';
        }
      }
    );
  }
}
