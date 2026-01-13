# RBAC Quick Reference Card

## 🎯 Three Roles

| Role | Code | Can Do |
|------|------|--------|
| **Student** | `student` | Submit clearances, view own data |
| **Dept Staff** | `department_staff` | Approve for assigned dept only |
| **Admin** | `admin` | Full system access |

---

## 🔒 Permission Classes (Import from `apps.users.permissions`)

### Basic Role Checks
```python
from apps.users.permissions import IsAdmin, IsDepartmentStaff, IsStudent

# Use in ViewSet
permission_classes = [IsAuthenticated, IsAdmin]
```

### Combined Role Permissions
```python
from apps.users.permissions import IsAdminOrDepartmentStaff

permission_classes = [IsAuthenticated, IsAdminOrDepartmentStaff]
```

### Object-Level Permissions
```python
from apps.users.permissions import IsStudentOwnerOrAdmin

# Students see own records, admins see all
permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]

# Must also filter queryset:
def get_queryset(self):
    if self.request.user.role == 'student':
        return Model.objects.filter(user=self.request.user)
    return Model.objects.all()
```

### Approval Permissions
```python
from apps.users.permissions import CanApproveClearance

# Checks department assignment for staff
permission_classes = [IsAuthenticated, CanApproveClearance]
```

### Read/Write Control
```python
from apps.users.permissions import IsAdminOrReadOnly

# All users can read, only admins can write
permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
```

---

## 📋 Common Patterns

### Pattern 1: Students See Own, Admins See All
```python
class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.role == 'student':
            return MyModel.objects.filter(user=self.request.user)
        return MyModel.objects.all()
```

### Pattern 2: All Read, Admin Write
```python
class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    # No queryset filtering needed - all can read
```

### Pattern 3: Different Permissions Per Action
```python
def get_permissions(self):
    if self.action == 'create':
        return [IsAuthenticated(), IsAdmin()]
    elif self.action in ['approve', 'reject']:
        return [IsAuthenticated(), CanApproveClearance()]
    return [IsAuthenticated()]
```

### Pattern 4: Department-Specific Access
```python
class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CanApproveClearance]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return MyModel.objects.all()
        elif user.role == 'department_staff':
            return MyModel.objects.filter(department=user.department)
        return MyModel.objects.none()
```

---

## 🔑 User Model Fields

```python
user.role                    # 'student', 'department_staff', or 'admin'
user.department              # Department FK (for dept staff only)
user.department.name         # Department name
user.department.code         # Department code
```

---

## ✅ Permission Checks in Views

### Check Role
```python
if request.user.role == 'admin':
    # Admin-specific logic
elif request.user.role == 'department_staff':
    # Staff-specific logic
elif request.user.role == 'student':
    # Student-specific logic
```

### Check Department Assignment
```python
if request.user.role == 'department_staff':
    if not request.user.department:
        return Response({"error": "No department assigned"}, status=403)
    
    if obj.department != request.user.department:
        return Response({"error": "Wrong department"}, status=403)
```

### Check Ownership
```python
if request.user.role == 'student':
    if obj.student.user != request.user:
        return Response({"error": "Not your record"}, status=403)
```

---

## 🧪 Testing Access Control

### 1. Login as Different Roles
```python
# Login as student
POST /api/auth/login/
{"email": "student@mksu.ac.ke", "password": "student123"}

# Login as staff
POST /api/auth/login/
{"email": "staff@mksu.ac.ke", "password": "staff123"}

# Login as admin
POST /api/auth/login/
{"email": "admin@mksu.ac.ke", "password": "admin123"}
```

### 2. Check Token Payload
```python
import jwt
payload = jwt.decode(token, options={"verify_signature": False})
print(payload['role'])         # User role
print(payload['email'])        # User email
```

### 3. Run Permission Tests
```bash
cd BACKEND
python test_permissions.py
```

---

## 🚨 Common Mistakes

### ❌ Forgetting Queryset Filtering
```python
# Wrong - all users see all records!
class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()  # ❌
```

```python
# Right - students see only own records
class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]
    
    def get_queryset(self):  # ✅
        if self.request.user.role == 'student':
            return Student.objects.filter(user=self.request.user)
        return Student.objects.all()
```

### ❌ Not Checking Department Assignment
```python
# Wrong - any staff can approve
if request.user.role == 'department_staff':
    approval.approve()  # ❌
```

```python
# Right - check department
if request.user.role == 'department_staff':
    if approval.department != request.user.department:  # ✅
        return Response({"error": "Wrong department"}, status=403)
    approval.approve()
```

### ❌ Using Wrong Permission Class
```python
# Wrong - too permissive
permission_classes = [IsAuthenticated]  # ❌

# Right - proper RBAC
permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]  # ✅
```

---

## 📊 Permission Matrix

| Endpoint | Student | Dept Staff | Admin |
|----------|---------|------------|-------|
| `GET /students/me/` | ✅ Own | ❌ | ✅ All |
| `GET /students/` | ✅ Own | ❌ | ✅ All |
| `POST /students/` | ❌ | ❌ | ✅ |
| `GET /clearances/` | ✅ Own | ✅ All | ✅ All |
| `POST /clearances/` | ✅ | ❌ | ✅ |
| `GET /approvals/` | ❌ | ✅ Dept | ✅ All |
| `POST /approvals/{id}/approve/` | ❌ | ✅ Dept | ✅ |
| `GET /departments/` | ✅ | ✅ | ✅ |
| `POST /departments/` | ❌ | ❌ | ✅ |
| `GET /finance/my_payment/` | ✅ Own | ❌ | ✅ All |
| `POST /finance/{id}/verify/` | ❌ | ❌ | ✅ |
| `GET /audit-logs/` | ❌ | ❌ | ✅ |
| `GET /analytics/` | ❌ | ✅ | ✅ |

✅ = Allowed  
❌ = Denied  
Own = Own records only  
Dept = Own department only  
All = All records

---

## 🔧 Setup Department Staff

### Via Admin Panel
1. Go to Users
2. Edit user
3. Set Role = "Department Staff"
4. Select Department
5. Save

### Via API
```python
PATCH /api/users/{id}/
{
  "role": "department_staff",
  "department": 2  # Department ID
}
```

### Via Django Shell
```python
from apps.users.models import User
from apps.departments.models import Department

user = User.objects.get(email='staff@mksu.ac.ke')
dept = Department.objects.get(code='FIN')
user.role = 'department_staff'
user.department = dept
user.save()
```

---

## 📚 Resources

- **Full Guide**: `BACKEND/RBAC_IMPLEMENTATION_GUIDE.md`
- **Summary**: `BACKEND/RBAC_IMPLEMENTATION_SUMMARY.md`
- **Permission Classes**: `apps/users/permissions.py`
- **Test Suite**: `BACKEND/test_permissions.py`

---

**Quick Help**: If permission denied (403), check:
1. User is authenticated ✅
2. User has correct role ✅
3. Permission class is correct ✅
4. Queryset is filtered properly ✅
5. Department staff has department assigned ✅
