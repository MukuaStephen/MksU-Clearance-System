import { Injectable } from '@angular/core';

export interface ClearanceRecord {
  office: string;
  status: 'Not Submitted' | 'Pending' | 'Approved' | 'Denied';
  submittedAt?: Date;
}

@Injectable({
  providedIn: 'root'
})
export class ClearanceService {

  private records: ClearanceRecord[] = [
    { office: 'Chairperson of Department', status: 'Not Submitted' },
    { office: 'Hostel', status: 'Not Submitted' },
    { office: 'Mess', status: 'Not Submitted' },
    { office: 'Sports & Games', status: 'Not Submitted' },
    { office: 'Workshops', status: 'Not Submitted' },
    { office: 'Finance', status: 'Not Submitted' },
    { office: 'Library', status: 'Not Submitted' }
  ];

  getAllRecords() {
    return this.records;
  }

  submitClearance(office: string) {
    const record = this.records.find(r => r.office === office);
    if (record && record.status === 'Not Submitted') {
      record.status = 'Pending';
      record.submittedAt = new Date();
    }
  }
}
