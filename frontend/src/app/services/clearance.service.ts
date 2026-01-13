import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ApiService } from './api.service';

export interface ClearanceRecord {
  office: string;
  status: 'Not Submitted' | 'Pending' | 'Approved' | 'Denied';
  submittedAt?: Date;
  id?: number;
}

@Injectable({
  providedIn: 'root'
})
export class ClearanceService {

  private recordsSubject = new BehaviorSubject<ClearanceRecord[]>([]);
  public records$ = this.recordsSubject.asObservable();

  constructor(private apiService: ApiService) {
    this.loadClearanceStatus();
  }

  loadClearanceStatus(): void {
    const userId = this.apiService.getUserId();
    if (!userId) {
      // Set default records if not authenticated
      this.setDefaultRecords();
      return;
    }

    // Load clearance status from backend
    this.apiService.getClearances({ student: userId }).subscribe(
      (response: any) => {
        const clearances = Array.isArray(response) ? response : response.results || [];
        
        if (clearances.length > 0) {
          // Map backend data to records
          const records = this.mapClearancesToRecords(clearances);
          this.recordsSubject.next(records);
        } else {
          // No clearances yet, show default departments
          this.setDefaultRecords();
        }
      },
      (error: any) => {
        console.error('Error loading clearances:', error);
        this.setDefaultRecords();
      }
    );
  }

  private mapClearancesToRecords(clearances: any[]): ClearanceRecord[] {
    // Get unique departments from clearances
    const departments = ['Finance', 'Library', 'Mess/Cafeteria', 'Hostel', 
                        'Academic Affairs', 'Workshop/Labs', 'Sports & Games', 'Student Services'];
    
    return departments.map(dept => {
      const clearance = clearances.find(c => c.department === dept);
      return {
        office: dept,
        status: clearance ? this.mapStatus(clearance.status) : 'Not Submitted',
        submittedAt: clearance?.created_at ? new Date(clearance.created_at) : undefined,
        id: clearance?.id
      };
    });
  }

  private mapStatus(backendStatus: string): 'Not Submitted' | 'Pending' | 'Approved' | 'Denied' {
    switch(backendStatus.toLowerCase()) {
      case 'approved':
      case 'completed':
        return 'Approved';
      case 'rejected':
      case 'denied':
        return 'Denied';
      case 'pending':
      case 'in_progress':
        return 'Pending';
      default:
        return 'Not Submitted';
    }
  }

  private setDefaultRecords(): void {
    const records: ClearanceRecord[] = [
      { office: 'Finance', status: 'Not Submitted' },
      { office: 'Library', status: 'Not Submitted' },
      { office: 'Mess/Cafeteria', status: 'Not Submitted' },
      { office: 'Hostel', status: 'Not Submitted' },
      { office: 'Academic Affairs', status: 'Not Submitted' },
      { office: 'Workshop/Labs', status: 'Not Submitted' },
      { office: 'Sports & Games', status: 'Not Submitted' },
      { office: 'Student Services', status: 'Not Submitted' }
    ];
    this.recordsSubject.next(records);
  }

  getAllRecords(): ClearanceRecord[] {
    return this.recordsSubject.value;
  }

  submitClearance(office: string): Observable<any> {
    const userId = this.apiService.getUserId();
    
    if (!userId) {
      throw new Error('User not authenticated');
    }

    // Create clearance request via API
    const clearanceData = {
      student: userId,
      clearance_type: 'graduation',
      status: 'pending'
    };

    return this.apiService.createClearance(clearanceData).pipe(
      tap(() => {
        // Reload clearance status after submission
        this.loadClearanceStatus();
      })
    );
  }
}
