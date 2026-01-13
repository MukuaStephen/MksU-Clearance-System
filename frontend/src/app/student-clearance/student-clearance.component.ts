import { Component } from '@angular/core';
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
export class StudentClearanceComponent {

  selectedReason: string = '';

  records: ClearanceRecord[] = [];

  constructor(private clearanceService: ClearanceService) {
    this.records = this.clearanceService.getAllRecords();
  }

  submit(office: string): void {
    this.clearanceService.submitClearance(office);
  }
}
