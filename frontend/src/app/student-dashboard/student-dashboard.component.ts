import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { StudentClearanceComponent } from '../student-clearance/student-clearance.component';
import { ClearanceService } from '../services/clearance.service';

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
export class StudentDashboardComponent {

  activeView: 'dashboard' | 'clearance' | 'profile' = 'dashboard';

  oldPassword: string = '';
  newPassword: string = '';
  passwordMessage: string = '';

  constructor(
    public clearanceService: ClearanceService,
    private router: Router
  ) {}

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
    this.router.navigate(['/']);
  }

  changePassword(): void {
    if (!this.oldPassword || !this.newPassword) {
      this.passwordMessage = 'Please fill in both password fields.';
      return;
    }

    this.passwordMessage = 'Password changed successfully.';
    this.oldPassword = '';
    this.newPassword = '';
  }
}
