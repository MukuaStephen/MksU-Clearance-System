import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-student-clearance',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './student-clearance.component.html',
  styleUrls: ['./student-clearance.component.css']
})
export class StudentClearanceComponent {

  selectedReason = '';

  offices = [
    'Chairperson of Department',
    'Hostel',
    'Mess',
    'Sports & Games',
    'Workshops',
    'Finance',
    'Library'
  ];

  submit(office: string) {
    alert(`Clearance request sent to ${office}`);
  }
}
