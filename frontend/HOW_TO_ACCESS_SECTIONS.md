# 🎓 Access Different User Sections

Your application now has **3 separate portals** with different dashboards for each user role.

---

## 🚀 Quick Access Guide

### 1. **Student Portal** 👨‍🎓
- **URL:** http://localhost:4200/
- **Or:** http://localhost:4200/login
- **Dashboard:** http://localhost:4200/dashboard
- **What You Can Do:**
  - Register for an account
  - Login to your profile
  - Submit clearance requests
  - Track clearance status
  - View assigned departments
  - Check payment status
  - Receive notifications

---

### 2. **Staff Portal** 👨‍💼
- **URL:** http://localhost:4200/staff-login
- **Dashboard:** http://localhost:4200/staff/dashboard
- **What You Can Do:**
  - Login as department staff
  - View pending clearance requests from students
  - Filter requests by status (Pending, Approved, Rejected)
  - Approve or reject clearances
  - View student details
  - Generate reports

---

### 3. **Admin Portal** 🔐
- **URL:** http://localhost:4200/admin-login
- **Dashboard:** http://localhost:4200/admin/dashboard
- **What You Can Do:**
  - Login as system administrator
  - View system statistics (total students, staff, clearances)
  - Manage all users (students, staff, admins)
  - Add or delete users
  - Configure system settings
  - Enable/disable features
  - Backup database
  - View system logs

---

## 📱 Navigation Map

```
http://localhost:4200/
    ↓
    ├─→ Student Login (/login)
    │   └─→ Student Dashboard (/dashboard)
    │
    ├─→ Staff Login (/staff-login)
    │   └─→ Staff Dashboard (/staff/dashboard)
    │
    └─→ Admin Login (/admin-login)
        └─→ Admin Dashboard (/admin/dashboard)
```

---

## 🔑 Test Credentials (To Be Implemented)

Once you integrate with the backend API, use these credentials:

### Student
```
Email: student@mksu.ac.ke
Password: Student123!
```

### Staff
```
Email: staff@mksu.ac.ke
Password: Staff123!
```

### Admin
```
Email: admin@mksu.ac.ke
Password: Admin123!
```

---

## 🎯 Current Status

| Section | Status | Features |
|---------|--------|----------|
| **Student Section** | ✅ UI Ready | Login, Dashboard (needs API integration) |
| **Staff Section** | ✅ UI Ready | Login, View Clearances, Approve/Reject (needs API integration) |
| **Admin Section** | ✅ UI Ready | Login, Dashboard, Users Management, Settings (needs API integration) |

---

## ⚙️ Features by Portal

### Student Portal Features
- ✅ Login/Register
- ✅ View Profile
- ✅ Submit Clearance Request
- ✅ Track Status
- ✅ View Notifications
- ✅ Check Payment Status

### Staff Portal Features
- ✅ View All Clearance Requests
- ✅ Filter by Status (Pending/Approved/Rejected)
- ✅ Approve Clearances
- ✅ Reject Clearances
- ✅ View Student Details
- ✅ Add Comments/Notes
- ✅ Download Reports

### Admin Portal Features
- ✅ System Dashboard with Statistics
- ✅ View All Users (Students, Staff, Admins)
- ✅ Create/Edit/Delete Users
- ✅ System Configuration
- ✅ Enable/Disable Features
- ✅ Database Backup
- ✅ View Audit Logs
- ✅ Generate Reports

---

## 🔗 Frontend to Backend Integration

Currently, the frontend has **UI components only**. The next step is to connect them to the backend API:

### Backend API Endpoints Available

**Authentication:**
```
POST /api/auth/register/        - Register
POST /api/auth/login/           - Login
POST /api/auth/token/           - Get JWT Token
POST /api/auth/logout/          - Logout
```

**Students:**
```
GET /api/students/              - List students
POST /api/students/             - Create student
GET /api/students/{id}/         - Get student details
```

**Clearances:**
```
GET /api/clearances/            - List clearances
POST /api/clearances/           - Submit clearance
GET /api/clearances/{id}/       - Get clearance details
PUT /api/clearances/{id}/       - Update clearance
```

**Approvals (Staff Only):**
```
GET /api/approvals/             - List approvals
POST /api/approvals/            - Create approval
PUT /api/approvals/{id}/        - Update approval status
```

**Departments:**
```
GET /api/departments/           - List departments
GET /api/departments/{id}/      - Get department details
```

See **Backend API docs** at http://localhost:8000/api/docs/ for complete endpoint list.

---

## 🔄 How to Connect Frontend to Backend

### Step 1: Create API Service
```typescript
// src/app/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/login/`, { email, password });
  }

  getClearances(): Observable<any> {
    return this.http.get(`${this.baseUrl}/clearances/`);
  }

  approveClearance(id: number): Observable<any> {
    return this.http.put(`${this.baseUrl}/approvals/${id}/`, { status: 'approved' });
  }
}
```

### Step 2: Use Service in Components
```typescript
// In staff-dashboard.component.ts
export class StaffDashboardComponent implements OnInit {
  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getClearances().subscribe(
      (data) => this.clearances = data,
      (error) => console.error('Error loading clearances', error)
    );
  }

  approveClearance(id: number) {
    this.apiService.approveClearance(id).subscribe(
      (response) => alert('Clearance approved!'),
      (error) => alert('Error approving clearance')
    );
  }
}
```

### Step 3: Add HttpClientModule
```typescript
// src/app/app.config.ts
import { HttpClientModule } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    importProvidersFrom(HttpClientModule)
  ]
};
```

---

## 🌐 Access from Different Devices

### From Your Computer
```
Student:  http://localhost:4200/
Staff:    http://localhost:4200/staff-login
Admin:    http://localhost:4200/admin-login
```

### From Another Computer (on same network)
```
Find your IP address: ipconfig (Windows) or ifconfig (Mac/Linux)
Example IP: 192.168.1.100

Student:  http://192.168.1.100:4200/
Staff:    http://192.168.1.100:4200/staff-login
Admin:    http://192.168.1.100:4200/admin-login
```

---

## 🧪 Testing Workflow

1. **Start Both Servers:**
   ```powershell
   # Terminal 1 - Backend
   cd BACKEND
   python manage.py runserver 8000

   # Terminal 2 - Frontend
   cd FRONTEND
   npm start
   ```

2. **Test Student Flow:**
   - Open http://localhost:4200/
   - See login page
   - (Once API connected) Register new student
   - Login to dashboard
   - Submit clearance request

3. **Test Staff Flow:**
   - Open http://localhost:4200/staff-login
   - (Once API connected) Login as staff
   - View clearance requests
   - Approve/Reject requests

4. **Test Admin Flow:**
   - Open http://localhost:4200/admin-login
   - (Once API connected) Login as admin
   - View system statistics
   - Manage users

---

## 📊 Component Structure

```
FRONTEND/src/app/
├── student-login/
│   ├── student-login.component.ts
│   ├── student-login.component.html
│   └── student-login.component.css
├── student-dashboard/
│   ├── student-dashboard.component.ts
│   ├── student-dashboard.component.html
│   └── student-dashboard.component.css
├── staff-login/
│   ├── staff-login.component.ts
│   ├── staff-login.component.html
│   └── staff-login.component.css
├── staff-dashboard/
│   ├── staff-dashboard.component.ts
│   ├── staff-dashboard.component.html
│   └── staff-dashboard.component.css
├── admin-login/
│   ├── admin-login.component.ts
│   ├── admin-login.component.html
│   └── admin-login.component.css
├── admin-dashboard/
│   ├── admin-dashboard.component.ts
│   ├── admin-dashboard.component.html
│   └── admin-dashboard.component.css
├── app.routes.ts (Updated with all routes)
└── app.config.ts
```

---

## ✅ Next Steps

1. **Visit the portals** to see the UI
2. **Create API Service** to connect to backend
3. **Implement API calls** in each component
4. **Add JWT token management** (store/use tokens)
5. **Add authentication guards** to protect routes
6. **Add error handling** for API failures
7. **Deploy to production** when ready

---

**Ready to explore?** Visit:
- 🎓 Student: http://localhost:4200/
- 👨‍💼 Staff: http://localhost:4200/staff-login
- 🔐 Admin: http://localhost:4200/admin-login
