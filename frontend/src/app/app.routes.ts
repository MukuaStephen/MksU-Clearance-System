import { Routes } from '@angular/router';
import { StudentLoginComponent } from './student-login/student-login.component';
import { StudentDashboardComponent } from './student-dashboard/student-dashboard.component';

export const routes: Routes = [
  { path: '', component: StudentLoginComponent },
  { path: 'dashboard', component: StudentDashboardComponent },
  { path: '**', redirectTo: '' }
];
