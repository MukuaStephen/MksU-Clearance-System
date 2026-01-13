import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';

interface SystemStats {
  totalStudents: number;
  totalStaff: number;
  pendingClearances: number;
  completedClearances: number;
}

interface SystemUser {
  id: number;
  email: string;
  full_name: string;
  role: string;
  created_at: string;
}

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {
  stats: SystemStats = {
    totalStudents: 0,
    totalStaff: 0,
    pendingClearances: 0,
    completedClearances: 0
  };

  users: SystemUser[] = [];
  newUser = {
    email: '',
    full_name: '',
    role: 'student', // Default role
    password: ''
  };
  activeTab: string = 'dashboard';
  loading: boolean = false;
  error: string = '';
  showAddUserForm = false;

  constructor(private router: Router, private apiService: ApiService) {}

  ngOnInit() {
    // Check if user is authenticated
    if (!this.apiService.isAuthenticated()) {
      this.router.navigate(['/admin-login']);
      return;
    }

    this.loadDashboardData();
  }

  loadDashboardData() {
    this.loading = true;
    this.error = '';

    // Load all data
    this.apiService.getStudents().subscribe(
      (response: any) => {
        this.stats.totalStudents = Array.isArray(response) ? response.length : response.count || 0;
        this.loadMoreData();
      },
      (error: any) => {
        console.error('Error loading students:', error);
        this.loadMoreData();
      }
    );
  }

  private loadMoreData() {
    this.apiService.getApprovals().subscribe(
      (response: any) => {
        const approvals = Array.isArray(response) ? response : response.results || [];
        this.stats.pendingClearances = approvals.filter((a: any) => a.status === 'pending').length;
        this.stats.completedClearances = approvals.filter((a: any) => a.status === 'approved').length;
        this.loading = false;
      },
      (error: any) => {
        console.error('Error loading approvals:', error);
        this.loading = false;
        if (error.status === 401) {
          this.router.navigate(['/admin-login']);
        }
      }
    );
  }

  switchTab(tab: string) {
    this.activeTab = tab;
    if (tab === 'users') {
      this.loadUsers();
    }
  }

  loadUsers() {
    this.loading = true;

    this.apiService.getStudents().subscribe(
      (response: any) => {
        const students = Array.isArray(response) ? response : response.results || [];
        this.users = students.map((s: any) => ({
          id: s.id,
          email: s.email,
          full_name: s.full_name,
          role: 'student',
          created_at: s.created_at || new Date().toISOString()
        }));
        this.loading = false;
      },
      (error: any) => {
        console.error('Error loading users:', error);
        this.loading = false;
      }
    );
  }

  deleteUser(id: number) {
    if (confirm('Are you sure you want to delete this user?')) {
      this.apiService.deleteStudent(id).subscribe(
        () => {
          alert('User deleted successfully!');
          this.loadUsers();
        },
        (error: any) => {
          alert('Error deleting user: ' + (error.error?.detail || 'Unknown error'));
          console.error('Error deleting user:', error);
        }
      );
    }
  }

  viewUserDetails(id: number) {
    this.router.navigate(['/admin/user', id]);
  }

  logout() {
    this.apiService.logout().subscribe(
      () => {
        this.router.navigate(['/admin-login']);
      },
      (error: any) => {
        // Still redirect even if logout fails
        localStorage.clear();
        this.router.navigate(['/admin-login']);
      }
    );
  }

  toggleAddUserForm(): void {
    this.showAddUserForm = !this.showAddUserForm;
  }

  addUser(): void {
    if (!this.newUser.email || !this.newUser.full_name || !this.newUser.password) {
      alert('Please fill in all fields.');
      return;
    }

    this.apiService.addUser(this.newUser).subscribe(
      (response: any) => {
        alert('User added successfully!');
        this.loadUsers(); // Refresh the user list
        this.newUser = { email: '', full_name: '', role: 'student', password: '' }; // Reset form
        this.showAddUserForm = false; // Hide form
      },
      (error: any) => {
        alert('Error adding user: ' + (error.error?.detail || 'Unknown error'));
        console.error('Error adding user:', error);
      }
    );
  }
}
