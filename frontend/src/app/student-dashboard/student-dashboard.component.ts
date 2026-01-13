import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentClearanceComponent } from '../student-clearance/student-clearance.component';

@Component({
  selector: 'app-student-dashboard',
  standalone: true,
  imports: [CommonModule, StudentClearanceComponent],
  templateUrl: './student-dashboard.component.html',
  styleUrls: ['./student-dashboard.component.css']
})
export class StudentDashboardComponent {

  activeView: 'dashboard' | 'clearance' = 'dashboard';
  showClearanceMenu = false;

  showDashboard(): void {
    this.activeView = 'dashboard';
    this.showClearanceMenu = false;
  }

  toggleClearanceMenu(): void {
    this.showClearanceMenu = !this.showClearanceMenu;
  }

  openClearance(reason: string): void {
    console.log('Selected reason:', reason);
    this.activeView = 'clearance';
    this.showClearanceMenu = false;
  }
}
