# Role-Based Access Control (RBAC) Implementation Guide

## Overview

The MksU Clearance System implements a comprehensive Role-Based Access Control (RBAC) system to ensure that users can only access and modify data appropriate to their role in the university clearance process.

## System Roles

### 1. Student Role (`student`)

**Purpose**: For students going through the clearance process

**Permissions**:
- ✅ Submit clearance requests
- ✅ View own clearance status and history
- ✅ View own student profile
- ✅ Update own limited profile fields
- ✅ View own payment records
- ✅ Make payments
- ✅ View own notifications
- ✅ View own gown issuance information
- ❌ Cannot view other students' data
- ❌ Cannot approve/reject clearances
- ❌ Cannot access admin functions

**Key Endpoints**:
- `GET /api/students/me/` - Own profile
- `POST /api/clearances/` - Submit clearance request
- `GET /api/clearances/` - List own clearances only
- `GET /api/finance/my_payment/` - Own payment record
- `POST /api/finance/mpesa-stk-push/` - Make payment
- `GET /api/notifications/` - Own notifications

### 2. Department Staff Role (`department_staff`)

**Purpose**: For staff members who approve clearances for their department

**Permissions**:
- ✅ View clearances requiring their department's approval
- ✅ Approve/reject clearances for their assigned department only
- ✅ Add notes and evidence to approvals
- ✅ View student details (for clearance processing)
- ✅ View payment records (for verification)
- ✅ View department statistics
- ✅ Receive notifications about pending approvals
- ❌ Cannot approve clearances for other departments
- ❌ Cannot modify department settings
- ❌ Cannot access audit logs
- ❌ Cannot manage users

**Department Assignment**:
Each department staff member MUST be assigned to a department via the `department` field in the User model. This assignment determines which clearances they can approve.

**Key Endpoints**:
- `GET /api/approvals/` - List approvals (filtered to their department)
- `GET /api/approvals/pending/` - Pending approvals for their department
- `POST /api/approvals/{id}/approve/` - Approve clearance (department check enforced)
- `POST /api/approvals/{id}/reject/` - Reject clearance (department check enforced)
- `GET /api/analytics/dashboard/` - Department analytics

### 3. Admin Role (`admin`)

**Purpose**: For system administrators with full access

**Permissions**:
- ✅ Full CRUD access to all resources
- ✅ User management (create, edit, delete users)
- ✅ Department management
- ✅ Approve/reject any clearance
- ✅ Override clearance decisions
- ✅ Verify payments
- ✅ Access audit logs
- ✅ View all analytics and reports
- ✅ Manage gown issuances
- ✅ System configuration

**Key Endpoints**:
- All endpoints with full permissions
- `GET /api/audit-logs/` - Access audit logs
- `POST /api/users/` - Create users
- `POST /api/departments/` - Create departments
- `POST /api/finance/{id}/verify/` - Verify payments

---

## Permission Classes

The system uses custom Django REST Framework permission classes located in `apps/users/permissions.py`:

### Role-Based Permissions

#### `IsAdmin`
Allows access only to users with `role='admin'`

```python
permission_classes = [IsAuthenticated, IsAdmin]
```

#### `IsDepartmentStaff`
Allows access only to users with `role='department_staff'`

```python
permission_classes = [IsAuthenticated, IsDepartmentStaff]
```

#### `IsStudent`
Allows access only to users with `role='student'`

```python
permission_classes = [IsAuthenticated, IsStudent]
```

#### `IsAdminOrDepartmentStaff`
Allows access to both admins and department staff

```python
permission_classes = [IsAuthenticated, IsAdminOrDepartmentStaff]
```

### Object-Level Permissions

#### `IsOwnerOrAdmin`
Allows object access to the owner (checks `obj.user == request.user`) or any admin

```python
permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
```

#### `IsStudentOwnerOrAdmin`
Students can only access their own records; admins can access all records. Automatically filters querysets based on role.

```python
permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]
```

**Queryset Filtering Example**:
```python
def get_queryset(self):
    if self.request.user.role == 'admin':
        return Student.objects.all()
    elif self.request.user.role == 'student':
        return Student.objects.filter(user=self.request.user)
    return Student.objects.none()
```

#### `CanApproveClearance`
**Enhanced with Department Assignment Check**

Allows approval actions only if:
- User is admin (can approve any clearance), OR
- User is department staff AND is assigned to the approval's department

```python
def has_object_permission(self, request, view, obj):
    if request.user.role == 'admin':
        return True
    
    if request.user.role == 'department_staff':
        # Check department assignment
        if not request.user.department:
            return False
        return obj.department == request.user.department
    
    return False
```

### Read/Write Control

#### `ReadOnly`
Allows only GET, HEAD, OPTIONS methods

```python
permission_classes = [IsAuthenticated, ReadOnly]
```

#### `IsAdminOrReadOnly`
All authenticated users can read; only admins can create/update/delete

```python
permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
```

**Usage Example**:
```python
class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    # All users can GET departments
    # Only admins can POST, PUT, PATCH, DELETE
```

---

## Implementation by App

### Students App
- **List/Retrieve**: `IsStudentOwnerOrAdmin` - Students see own, admins see all
- **Create**: `IsAdmin` only
- **Update**: `IsStudentOwnerOrAdmin` - Limited fields for students
- **Delete**: `IsAdmin` only

### Clearances App
- **List**: Students see own requests, staff/admins see all
- **Create**: Students only (with eligibility checks)
- **Update**: Students can update drafts, admins can update any
- **Delete**: `IsAdmin` only

### Approvals App
- **List**: Department staff see their department, admins see all
- **Retrieve**: `CanApproveClearance`
- **Approve/Reject**: `CanApproveClearance` with department assignment check
- **Update**: Department staff for their dept, admins for all
- **Delete**: `IsAdmin` only

### Finance App
- **List/Retrieve**: Students see own payment, admins/staff see all
- **Create**: Students (for themselves), admins (for any)
- **Verify**: `IsAdmin` only
- **Update/Delete**: `IsAdmin` only

### Departments App
- **List/Retrieve**: All authenticated users (read-only)
- **Create/Update/Delete**: `IsAdmin` only

### Notifications App
- **List**: Users see only their own notifications
- **Mark as read**: Own notifications only
- **Create**: System-generated only

### Audit Logs App
- **All operations**: `IsAdmin` only

### Gown Issuance App
- **All operations**: `IsAdmin` only

### Analytics App
- **All operations**: `IsAdminOrDepartmentStaff`

---

## Department Assignment Workflow

### Setting Up Department Staff

1. **Create User with department_staff role**:
```bash
POST /api/auth/register/
{
  "email": "finance.staff@mksu.ac.ke",
  "full_name": "Finance Staff Member",
  "password": "SecurePass123",
  "role": "department_staff",
  "department": 1  // Finance Department ID
}
```

2. **Update Existing User**:
```bash
PATCH /api/users/{id}/
{
  "role": "department_staff",
  "department": 2  // Library Department ID
}
```

3. **Via Django Admin**:
   - Navigate to Users section
   - Edit user
   - Set Role to "Department Staff"
   - Select Department from dropdown
   - Save

### Important Notes

- ✅ Department assignment is **required** for department staff to approve clearances
- ✅ Staff without department assignment will be denied when trying to approve
- ✅ Staff can only approve clearances for their assigned department
- ✅ Admins don't need department assignment (they have universal access)
- ✅ Students don't use the department field (it's for staff only)

---

## Testing RBAC

### Running Permission Tests

```bash
cd BACKEND
python test_permissions.py
```

This will test:
- ✅ Authentication endpoints
- ✅ Department permissions (read for all, write for admins)
- ✅ Student object-level permissions
- ✅ Department actions
- ✅ Role-based access control

### Manual Testing

1. **Create Test Users**:
```bash
python create_test_users.py
```

Creates:
- `admin@mksu.ac.ke` (Admin role)
- `student@mksu.ac.ke` (Student role)
- `staff@mksu.ac.ke` (Department Staff with Finance department)

2. **Test Authentication**:
```bash
# Login as student
POST /api/auth/login/
{
  "email": "student@mksu.ac.ke",
  "password": "student123"
}

# Response includes JWT token and user data with role
```

3. **Test Permission Boundaries**:
```bash
# As student, try to access another student's data (should fail)
GET /api/students/{other_student_id}/
Authorization: Bearer {student_token}
# Expected: 403 Forbidden

# As admin, access any student data (should succeed)
GET /api/students/{any_student_id}/
Authorization: Bearer {admin_token}
# Expected: 200 OK with data
```

4. **Test Department Staff Permissions**:
```bash
# As department staff, approve clearance for assigned department
POST /api/approvals/{approval_id}/approve/
Authorization: Bearer {staff_token}
{
  "notes": "All requirements met"
}
# Expected: 200 OK if approval.department == user.department
# Expected: 403 Forbidden if approval.department != user.department
```

---

## Security Best Practices

### 1. Token Management
- Access tokens expire after 60 minutes
- Refresh tokens expire after 7 days
- Tokens are blacklisted on logout
- Store tokens securely in client (httpOnly cookies recommended)

### 2. Password Security
- Passwords are hashed using Django's default (PBKDF2)
- Password validation enforced on registration
- Minimum password requirements should be set

### 3. Audit Logging
- All sensitive actions are logged automatically via `AuditLogMiddleware`
- Logs include: user, action, IP address, timestamp, before/after data
- Audit logs are admin-only accessible

### 4. Rate Limiting
- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour
- Can be adjusted in `REST_FRAMEWORK` settings

### 5. CORS Configuration
- Only allowed origins can access the API
- Credentials (cookies) allowed only from trusted origins
- Configure in `CORS_ALLOWED_ORIGINS` setting

---

## Common Patterns

### Pattern 1: Admin-Only Write, Public Read
```python
class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    # GET: All authenticated users
    # POST/PUT/DELETE: Admins only
```

### Pattern 2: Owner or Admin Access
```python
class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.role == 'student':
            return Student.objects.filter(user=self.request.user)
        return Student.objects.all()
```

### Pattern 3: Action-Based Permissions
```python
def get_permissions(self):
    if self.action in ['create', 'destroy']:
        return [IsAuthenticated(), IsAdmin()]
    elif self.action in ['approve', 'reject']:
        return [IsAuthenticated(), CanApproveClearance()]
    return [IsAuthenticated()]
```

### Pattern 4: Custom Action with Department Check
```python
@action(detail=True, methods=['post'])
def approve(self, request, pk=None):
    approval = self.get_object()
    
    # Permission check is automatic via CanApproveClearance
    # But you can add additional business logic
    if request.user.role == 'department_staff':
        if request.user.department != approval.department:
            return Response(
                {"error": "You can only approve for your department"},
                status=403
            )
    
    # Process approval...
```

---

## Troubleshooting

### Issue: Department staff can't approve clearances

**Cause**: User not assigned to department

**Solution**:
```python
# Check if user has department
user = User.objects.get(email='staff@mksu.ac.ke')
print(user.department)  # Should not be None

# Assign department
from apps.departments.models import Department
finance_dept = Department.objects.get(code='FIN')
user.department = finance_dept
user.save()
```

### Issue: Students can see other students' data

**Cause**: ViewSet not using `IsStudentOwnerOrAdmin` permission or not filtering queryset

**Solution**:
```python
class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]  # ✅ Add this
    
    def get_queryset(self):  # ✅ Add queryset filtering
        if self.request.user.role == 'student':
            return Student.objects.filter(user=self.request.user)
        return Student.objects.all()
```

### Issue: 403 Forbidden for legitimate requests

**Cause**: Missing or incorrect permission class

**Solution**: Check permission classes in viewset:
```python
# Wrong:
permission_classes = [IsAuthenticated]  # Too permissive

# Right:
permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]  # Proper RBAC
```

---

## Migration from Previous System

If upgrading from a system without department assignment:

1. **Run Migration**:
```bash
python manage.py migrate users
```

2. **Assign Departments to Existing Staff**:
```python
from apps.users.models import User
from apps.departments.models import Department

# Get all department staff
staff = User.objects.filter(role='department_staff')

# Assign departments (you'll need to know which staff belongs to which dept)
finance_dept = Department.objects.get(code='FIN')
finance_staff = staff.filter(email__contains='finance')
finance_staff.update(department=finance_dept)
```

3. **Verify Assignments**:
```python
staff = User.objects.filter(role='department_staff', department__isnull=True)
if staff.exists():
    print(f"Warning: {staff.count()} staff members without department assignment")
```

---

## API Response Examples

### Successful Access (200 OK)
```json
{
  "id": 1,
  "email": "student@mksu.ac.ke",
  "full_name": "John Doe",
  "role": "student",
  "role_display": "Student",
  "department": null,
  "is_active": true
}
```

### Permission Denied (403 Forbidden)
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Department Check Failed (403 Forbidden)
```json
{
  "detail": "You can only approve clearances for your assigned department."
}
```

### Unauthenticated (401 Unauthorized)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## References

- **Permission Classes**: `apps/users/permissions.py`
- **User Model**: `apps/users/models.py`
- **Test Suite**: `BACKEND/test_permissions.py`
- **Task Completion Report**: `BACKEND/TASK5_COMPLETION_REPORT.md`
- **Django REST Framework Permissions**: https://www.django-rest-framework.org/api-guide/permissions/

---

**Last Updated**: January 13, 2026  
**Version**: 2.0 (Enhanced with Department Assignment)  
**Status**: ✅ Production Ready
