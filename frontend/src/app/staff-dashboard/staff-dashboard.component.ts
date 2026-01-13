import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';

interface ClearanceRequest {
  id: number;
  student_name: string;
  student_email: string;
  department: string;
  status: string;
  submitted_date: string;
}

@Component({
  selector: 'app-staff-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './staff-dashboard.component.html',
  styleUrls: ['./staff-dashboard.component.css']
})
export class StaffDashboardComponent implements OnInit {
  clearances: ClearanceRequest[] = [];
  filteredClearances: ClearanceRequest[] = [];
  filterStatus: string = 'all';
  loading: boolean = false;
  error: string = '';
  userEmail: string = '';

  constructor(private router: Router, private apiService: ApiService) {}

  ngOnInit() {
    // Check if user is authenticated
    if (!this.apiService.isAuthenticated()) {
      this.router.navigate(['/staff-login']);
      return;
    }

    this.userEmail = this.apiService.getUserEmail() || '';
    this.loadClearances();
  }

  loadClearances() {
    this.loading = true;
    this.error = '';

    const filters = this.filterStatus !== 'all' ? { status: this.filterStatus } : {};

    this.apiService.getApprovals(filters).subscribe(
      (response: any) => {
        this.clearances = response.results || response;
        this.filterClearances();
        this.loading = false;
      },
      (error: any) => {
        this.loading = false;
        console.error('Error loading clearances:', error);
        if (error.status === 401) {
          this.router.navigate(['/staff-login']);
        } else {
          this.error = 'Failed to load clearances. Please try again.';
        }
      }
    );
  }

  filterClearances() {
    if (this.filterStatus === 'all') {
      this.filteredClearances = this.clearances;
    } else {
      this.filteredClearances = this.clearances.filter(
        (c) => c.status === this.filterStatus
      );
    }
  }

  onFilterChange() {
    this.filterClearances();
  }

  approveClearance(id: number) {
    if (confirm('Are you sure you want to approve this clearance?')) {
      this.apiService.approveApproval(id, { status: 'approved' }).subscribe(
        (response: any) => {
          alert('Clearance approved successfully!');
          this.loadClearances();
        },
        (error: any) => {
          alert('Error approving clearance: ' + (error.error?.detail || 'Unknown error'));
          console.error('Error approving clearance:', error);
        }
      );
    }
  }

  rejectClearance(id: number) {
    const reason = prompt('Enter reason for rejection:');
    if (reason !== null) {
      this.apiService.rejectApproval(id, { status: 'rejected', reason }).subscribe(
        (response: any) => {
          alert('Clearance rejected successfully!');
          this.loadClearances();
        },
        (error: any) => {
          alert('Error rejecting clearance: ' + (error.error?.detail || 'Unknown error'));
          console.error('Error rejecting clearance:', error);
        }
      );
    }
  }

  viewDetails(id: number) {
    this.router.navigate(['/staff/clearance', id]);
  }

  logout() {
    this.apiService.logout().subscribe(
      () => {
        this.router.navigate(['/staff-login']);
      },
      (error: any) => {
        // Still redirect even if logout fails
        localStorage.clear();
        this.router.navigate(['/staff-login']);
      }
    );
  }
}
