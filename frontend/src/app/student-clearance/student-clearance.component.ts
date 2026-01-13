import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClearanceService, ClearanceRecord } from '../services/clearance.service';

@Component({
  selector: 'app-student-clearance',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './student-clearance.component.html',
  styleUrls: ['./student-clearance.component.css']
})
export class StudentClearanceComponent implements OnInit {

  selectedReason: string = '';
  records: ClearanceRecord[] = [];
  loading: boolean = false;
  error: string = '';

  constructor(private clearanceService: ClearanceService) {}

  ngOnInit() {
    // Subscribe to clearance records from service
    this.clearanceService.records$.subscribe(
      (records) => {
        this.records = records;
      }
    );
    
    // Initial load
    this.clearanceService.loadClearanceStatus();
  }

  submit(office: string): void {
    this.loading = true;
    this.error = '';

    this.clearanceService.submitClearance(office).subscribe(
      (response: any) => {
        this.loading = false;
        // Record will be updated via the service's reload
      },
      (error: any) => {
        this.loading = false;
        console.error('Error submitting clearance:', error);
        
        if (error.status === 0) {
          this.error = 'Cannot connect to server. Please ensure backend is running.';
        } else {
          this.error = 'Failed to submit clearance. Please try again.';
        }
      }
    );
  }
}
