import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface ClearanceOffice {
  name: string;
  status: 'Not Submitted' | 'Pending' | 'Approved' | 'Denied';
}

@Component({
  selector: 'app-clearance-office-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './clearance-office-list.component.html',
  styleUrls: ['./clearance-office-list.component.css']
})
export class ClearanceOfficeListComponent {

  // offices are passed from StudentClearanceComponent
  @Input() offices: ClearanceOffice[] = [];

  requestClearance(office: ClearanceOffice): void {
    if (office.status === 'Not Submitted') {
      office.status = 'Pending';
    }
  }
}
