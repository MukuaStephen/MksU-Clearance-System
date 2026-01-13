import { Routes } from '@angular/router';
import { StudentLoginComponent } from './student-login/student-login.component';
import { StudentDashboardComponent } from './student-dashboard/student-dashboard.component';
import { StaffDashboardComponent } from './staff-dashboard/staff-dashboard.component';
import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';

export const routes: Routes = [
  // Unified Login (for all user types - student, staff, admin)
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: StudentLoginComponent },
  
  // Redirect old staff/admin login routes to unified login
  { path: 'staff-login', redirectTo: 'login', pathMatch: 'full' },
  { path: 'admin-login', redirectTo: 'login', pathMatch: 'full' },

  // Student Routes
  { path: 'dashboard', component: StudentDashboardComponent },

  // Staff Routes
  { path: 'staff/dashboard', component: StaffDashboardComponent },
  { path: 'staff/clearance/:id', component: StaffDashboardComponent },

  // Admin Routes
  { path: 'admin/dashboard', component: AdminDashboardComponent },
  { path: 'admin/user/:id', component: AdminDashboardComponent },

  // Catch-all redirect
  { path: '**', redirectTo: 'login' }
];
