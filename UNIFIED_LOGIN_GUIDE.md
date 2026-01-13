# Unified Role-Based Login System

## Overview
The MksU Clearance System now uses a **single unified login page** that automatically routes users to the appropriate dashboard based on their role (Student, Staff, or Admin).

## How It Works

### 1. Single Entry Point
- **URL**: `http://localhost:4200/` or `http://localhost:4200/login`
- **All Users**: Students, Staff, and Admins all use the same login page
- **No Portal Selection**: Users don't need to choose which portal to access

### 2. Automatic Role-Based Routing

When you login, the system:
1. Sends credentials to backend (`/auth/login/`)
2. Backend validates and returns user data including `role` field
3. Frontend reads the role from response
4. Automatically navigates to correct dashboard:

```
Backend Role          →  Frontend Route
-----------------        -----------------
'student'            →  /dashboard
'department_staff'   →  /staff/dashboard
'admin'              →  /admin/dashboard
```

### 3. Security
- **Server-Side Role Verification**: Backend determines user role (secure)
- **JWT Token Authentication**: All requests include Bearer token
- **Role Cannot Be Modified Client-Side**: Frontend only reads role, doesn't set it

## Test Credentials

### Admin Account
```
Email: admin@mksu.ac.ke
Password: admin123
Role: admin
Lands on: http://localhost:4200/admin/dashboard
```

### Staff Account
```
Email: staff@mksu.ac.ke
Password: staff123
Role: department_staff
Lands on: http://localhost:4200/staff/dashboard
```

### Student Account
```
Email: student@example.com
Password: password123
Role: student
Lands on: http://localhost:4200/dashboard
```

## User Experience Flow

### For Students
1. Go to `http://localhost:4200/`
2. Click "Register as Student" to create account
3. Fill registration form (email, password, student ID, name, year, semester)
4. System logs you in automatically
5. Redirected to Student Dashboard

### For Staff/Admin
1. Go to `http://localhost:4200/`
2. Enter institutional email and password
3. System detects your role from backend
4. Redirected to Staff or Admin Dashboard automatically

## Route Redirects

The following routes all redirect to the unified login:
- `/` → `/login`
- `/staff-login` → `/login` (deprecated but redirected)
- `/admin-login` → `/login` (deprecated but redirected)

## Technical Implementation

### Frontend Components

**Login Component** (`student-login.component.ts`)
```typescript
login() {
  this.apiService.login(this.email, this.password).subscribe(
    (response: any) => {
      // Get role from backend response
      const userRole = response.user?.role || this.apiService.getUserRole();
      
      // Route based on role
      if (userRole === 'admin') {
        this.router.navigate(['/admin/dashboard']);
      } else if (userRole === 'department_staff') {
        this.router.navigate(['/staff/dashboard']);
      } else if (userRole === 'student') {
        this.router.navigate(['/dashboard']);
      } else {
        // Default fallback
        this.router.navigate(['/dashboard']);
      }
    }
  );
}
```

### Backend Response Format

**Login Endpoint** (`POST /auth/login/`)
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJh...",
  "refresh": "eyJ0eXAiOiJKV1QiLC...",
  "user": {
    "id": 1,
    "username": "admin@mksu.ac.ke",
    "email": "admin@mksu.ac.ke",
    "role": "admin",
    "first_name": "Admin",
    "last_name": "User"
  }
}
```

## Dashboard Features by Role

### Student Dashboard (`/dashboard`)
- View clearance status
- Submit clearance requests
- Track approvals
- View notifications
- Update profile

### Staff Dashboard (`/staff/dashboard`)
- View pending clearances
- Approve/Reject clearances
- Add comments/feedback
- View student details
- Track department approvals

### Admin Dashboard (`/admin/dashboard`)
- System statistics
- User management
- All clearances overview
- Department management
- System configuration

## Authentication Flow

```
User visits http://localhost:4200/
         ↓
    Login Page
         ↓
Enter Email & Password
         ↓
POST /auth/login/ (Backend)
         ↓
Backend validates credentials
         ↓
Returns JWT + User Data (with role)
         ↓
Frontend stores token in localStorage
         ↓
Reads user.role from response
         ↓
┌────────┬────────────┬────────┐
│student │dept_staff  │ admin  │
↓        ↓            ↓
/dashboard /staff/dashboard /admin/dashboard
```

## Benefits of Unified Login

✅ **Single URL**: Easy to remember and share
✅ **Automatic Routing**: No confusion about which portal to use
✅ **Secure**: Role determined by backend, not user choice
✅ **Consistent UX**: Same login experience for all users
✅ **Maintainable**: One login component instead of three
✅ **Mobile Friendly**: Simpler navigation structure

## Migration from Old System

### Old Way (Deprecated)
- Students: `http://localhost:4200/login`
- Staff: `http://localhost:4200/staff-login`
- Admin: `http://localhost:4200/admin-login`

### New Way (Current)
- **Everyone**: `http://localhost:4200/login`
- System automatically routes based on backend role

### Backward Compatibility
Old URLs still work (redirect to unified login):
- `/staff-login` → redirects to `/login`
- `/admin-login` → redirects to `/login`

## Future Enhancements

### Recommended Next Steps:
1. **Authentication Guards**: Protect routes based on role
   ```typescript
   { path: 'admin/dashboard', component: AdminDashboardComponent, canActivate: [AuthGuard, AdminGuard] }
   ```

2. **Role-Based Permissions**: Frontend components check permissions
   ```typescript
   *ngIf="hasPermission('approve_clearance')"
   ```

3. **Token Refresh**: Auto-refresh JWT before expiration
   ```typescript
   HTTP Interceptor → Detect 401 → Refresh token → Retry request
   ```

4. **Remember Me**: Store encrypted credentials (optional)

5. **Multi-Factor Authentication**: Add OTP for admin accounts

## Troubleshooting

### Issue: Redirected to wrong dashboard
**Solution**: Check backend user role in database
```sql
SELECT email, role FROM users_customuser WHERE email = 'your@email.com';
```

### Issue: Login successful but no redirect
**Solution**: Check browser console for errors, verify user.role exists in response

### Issue: 401 Unauthorized on API calls
**Solution**: Token may be expired, logout and login again

### Issue: Can't access staff/admin features
**Solution**: Verify user role in backend:
```python
# Django shell
from apps.users.models import CustomUser
user = CustomUser.objects.get(email='your@email.com')
print(user.role)  # Should be 'admin' or 'department_staff'
```

## API Integration

All authenticated requests include JWT token:
```typescript
headers: {
  'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
  'Content-Type': 'application/json'
}
```

Role-specific endpoints are protected on backend:
- Student endpoints: `IsStudent` permission
- Staff endpoints: `IsDepartmentStaff` permission
- Admin endpoints: `IsAdmin` permission

## Testing the System

1. **Start Backend**:
   ```powershell
   cd BACKEND
   .\start_server.bat
   ```

2. **Start Frontend**:
   ```powershell
   cd FRONTEND
   npm start
   ```

3. **Test Each Role**:
   - Login as admin → Should land on `/admin/dashboard`
   - Logout → Login as staff → Should land on `/staff/dashboard`
   - Logout → Login as student → Should land on `/dashboard`

4. **Verify API Calls**:
   - Open browser DevTools → Network tab
   - Watch for `/auth/login/` response containing user.role
   - Verify subsequent API calls include Authorization header

## Summary

The unified login system provides a seamless, secure, and user-friendly authentication experience. Users no longer need to know which portal to access—the system automatically determines the correct destination based on their role from the backend.

**One Login Page. Three Dashboards. Automatic Routing.** 🚀
