# MksU Clearance System - Backend API Schema & Data Structures

**Last Updated:** January 13, 2026  
**Status:** Complete Backend API Design

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Core Data Models](#core-data-models)
4. [API Endpoints](#api-endpoints)
5. [Data Structures (Request/Response)](#data-structures-requestresponse)
6. [Error Handling](#error-handling)
7. [Workflow Examples](#workflow-examples)

---

## System Overview

The MksU Clearance System is a Django REST Framework (DRF) backend that manages the university's graduation clearance workflow. It supports:

- **Role-Based Access Control (RBAC)**: Student, Department Staff, Administrator
- **Parallel Clearance Workflow**: Multiple departments approve simultaneously
- **Financial Integration**: M-PESA payment verification for graduation fees
- **Document Management**: File upload and evidence tracking
- **Audit Logging**: Complete activity tracking for compliance
- **Real-time Notifications**: Email notifications on status changes
- **Gown Issuance Management**: Gown assignment, return, and deposit tracking
- **Analytics & Reporting**: Completion rates, bottleneck analysis, financial summaries

---

## Authentication & Authorization

### JWT Authentication (SimpleJWT)

All authenticated endpoints require an `Authorization` header with a Bearer token:

```
Authorization: Bearer <access_token>
```

### Token Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth/token/` | POST | No | Obtain JWT token pair |
| `/api/auth/token/refresh/` | POST | No | Refresh access token |

### Token Request/Response

**Request:**
```json
{
  "email": "student@mksu.ac.ke",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Role-Based Permissions

| Role | Endpoints | Scope |
|------|-----------|-------|
| **Student** | `/students/me/`, `/clearances/`, `/finance/my_payment/`, `/notifications/` | Own data only |
| **Department Staff** | `/approvals/` | Department-specific approvals |
| **Admin** | All endpoints | Full system access |

---

## Core Data Models

### 1. User Model
Represents all system users (students, staff, admins).

**Fields:**
```python
{
  "id": "uuid",
  "email": "student@mksu.ac.ke",
  "admission_number": "SCE/CS/0001/2024",
  "full_name": "John Doe",
  "role": "student|department_staff|admin",
  "is_active": true,
  "created_at": "2024-12-16T12:00:00Z",
  "updated_at": "2024-12-16T12:00:00Z"
}
```

**Role Choices:**
- `student` - Student user
- `department_staff` - Staff member of a department
- `admin` - System administrator

---

### 2. Student Model
Student profile linked to User model.

**Fields:**
```python
{
  "id": "uuid",
  "user_id": "uuid",
  "user": { User object },
  "registration_number": "SCE/CS/0001/2024",
  "admission_year": 2024,
  "faculty": "School of Computing and Engineering",
  "program": "Computer Science",
  "graduation_year": 2028,
  "school_id": "uuid",
  "department_id": "uuid",
  "course_id": "uuid",
  "eligibility_status": "pending|eligible|ineligible",
  "created_at": "2024-12-16T12:00:00Z",
  "updated_at": "2024-12-16T12:00:00Z"
}
```

**Registration Number Format:** `SCHOOL/DEPT/NNNN/YYYY`
- Example: `SCE/CS/0001/2024`
- Admission year is auto-extracted

---

### 3. Department Model
Represents clearance approval departments.

**Fields:**
```python
{
  "id": "uuid",
  "name": "Finance Office",
  "code": "FIN",
  "department_type": "finance|faculty|library|mess|hostel|workshop|sports|other",
  "head_email": "finance@mksu.ac.ke",
  "description": "Responsible for graduation fee verification",
  "is_active": true,
  "approval_order": 0,
  "created_at": "2024-12-16T12:00:00Z",
  "updated_at": "2024-12-16T12:00:00Z"
}
```

**Approval Order:**
- Departments with lower `approval_order` are processed first
- 0 = first to approve, higher numbers = later

---

### 4. ClearanceRequest Model
Student's clearance submission.

**Fields:**
```python
{
  "id": "uuid",
  "student_id": "uuid",
  "student": { Student object },
  "status": "pending|in_progress|completed|rejected",
  "submission_date": "2024-12-16T12:00:00Z",
  "completion_date": "2024-12-20T12:00:00Z",
  "rejection_reason": "Outstanding library fees",
  "completion_percentage": 75,
  "approval_summary": {
    "total": 8,
    "approved": 6,
    "rejected": 1,
    "pending": 1
  },
  "payment_status": {
    "has_paid": true,
    "amount": "5500.00",
    "payment_method": "mpesa",
    "verified": true
  },
  "created_at": "2024-12-16T12:00:00Z",
  "updated_at": "2024-12-16T12:00:00Z"
}
```

**Status Flow:**
```
pending → in_progress → completed
       ↘ rejected ↗
```

---

### 5. ClearanceApproval Model
Department's approval/rejection of a clearance request.

**Fields:**
```python
{
  "id": "uuid",
  "clearance_request_id": "uuid",
  "department_id": "uuid",
  "status": "pending|approved|rejected",
  "approved_by_id": "uuid",
  "approved_by": { User object },
  "approval_date": "2024-12-18T12:00:00Z",
  "rejection_reason": "Outstanding fees",
  "notes": "Cleared after fee payment",
  "evidence_file": "evidence/FIN/SCE-CS-0001-2024/receipt.pdf",
  "created_at": "2024-12-16T12:00:00Z",
  "updated_at": "2024-12-16T12:00:00Z"
}
```

**Constraint:** One approval per clearance request per department

---

### 6. FinanceRecord Model
Student's financial status for graduation.

**Fields:**
```python
{
  "id": "uuid",
  "student_id": "uuid",
  "tuition_balance": "0.00",
  "graduation_fee": "5500.00",
  "graduation_fee_status": "pending|paid|verified",
  "mpesa_code": "ABC123DEF456",
  "mpesa_payment_date": "2024-12-15T12:00:00Z",
  "last_verified_date": "2024-12-16T12:00:00Z",
  "verified_by": "Finance Staff Name",
  "notes": "Payment verified against MPESA logs",
  "created_at": "2024-12-16T12:00:00Z",
  "updated_at": "2024-12-16T12:00:00Z"
}
```

---

### 7. Payment Model
Payment record for graduation fees.

**Fields:**
```python
{
  "id": "uuid",
  "student_id": "uuid",
  "amount": "5500.00",
  "payment_method": "mpesa|bank|cash",
  "transaction_id": "MPS123456",
  "phone_number": "+254712345678",
  "payment_date": "2024-12-15T12:00:00Z",
  "is_verified": true,
  "verified_by_id": "uuid",
  "verification_date": "2024-12-16T12:00:00Z",
  "notes": "Verified against MPESA API",
  "receipt": "receipts/payment_12345.pdf",
  "created_at": "2024-12-16T12:00:00Z",
  "updated_at": "2024-12-16T12:00:00Z"
}
```

---

### 8. GownIssuance Model
Gown assignment and tracking.

**Fields:**
```python
{
  "id": "uuid",
  "student_id": "uuid",
  "gown_size": "S|M|L|XL|XXL",
  "gown_code": "GOWN001",
  "issue_date": "2024-12-17T12:00:00Z",
  "return_date": "2024-12-20T12:00:00Z",
  "deposit_amount": "1000.00",
  "deposit_paid": true,
  "deposit_refund_date": null,
  "deposit_status": "pending|retained|refunded",
  "is_returned": true,
  "notes": "Good condition",
  "created_at": "2024-12-16T12:00:00Z",
  "updated_at": "2024-12-16T12:00:00Z"
}
```

---

### 9. Notification Model
Real-time notification messages.

**Fields:**
```python
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Clearance Approved",
  "message": "Finance department has approved your clearance",
  "notification_type": "approval|rejection|payment|status_update|gown",
  "related_object_type": "clearance|approval|payment|gown",
  "related_object_id": "uuid",
  "is_read": false,
  "read_at": null,
  "created_at": "2024-12-16T12:00:00Z"
}
```

---

### 10. AuditLog Model
Audit trail for compliance.

**Fields:**
```python
{
  "id": "uuid",
  "user_id": "uuid",
  "action": "create|update|delete|approve|reject|verify",
  "content_type": "clearance|approval|payment|gown|user",
  "object_id": "uuid",
  "object_str": "Clearance Request - John Doe",
  "changes": {
    "status": ["pending", "approved"],
    "notes": [null, "Cleared after review"]
  },
  "ip_address": "192.168.1.100",
  "created_at": "2024-12-16T12:00:00Z"
}
```

---

## API Endpoints

### Authentication Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/token/` | No | Obtain JWT token pair |
| POST | `/api/auth/token/refresh/` | No | Refresh access token |
| POST | `/api/auth/register/` | No | Register new user |
| POST | `/api/auth/login/` | No | Login (alias for token obtain) |
| POST | `/api/auth/logout/` | Yes | Logout (blacklist token) |
| GET | `/api/auth/profile/` | Yes | Get current user profile |
| PUT | `/api/auth/profile/` | Yes | Update profile |
| PUT | `/api/auth/change-password/` | Yes | Change password |
| GET | `/api/auth/verify/` | Yes | Verify token validity |

---

### Student Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/students/` | Yes | Admin | List all students |
| POST | `/api/students/` | Yes | Admin | Create student |
| GET | `/api/students/{id}/` | Yes | Admin | Get student details |
| PUT | `/api/students/{id}/` | Yes | Admin | Update student |
| DELETE | `/api/students/{id}/` | Yes | Admin | Delete student |
| GET | `/api/students/me/` | Yes | Student | Get own profile |
| GET | `/api/students/{id}/clearance-status/` | Yes | - | Get clearance status |

---

### Clearance Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/clearances/` | Yes | - | List clearances |
| POST | `/api/clearances/` | Yes | Student | Submit clearance request |
| GET | `/api/clearances/{id}/` | Yes | - | Get clearance details |
| PUT | `/api/clearances/{id}/` | Yes | - | Update clearance |
| GET | `/api/clearances/{id}/approvals/` | Yes | - | Get all approvals for clearance |
| GET | `/api/clearances/{id}/progress/` | Yes | - | Get approval progress |

---

### Approval Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/approvals/` | Yes | Staff/Admin | List approvals |
| GET | `/api/approvals/{id}/` | Yes | Staff/Admin | Get approval details |
| POST | `/api/approvals/{id}/approve/` | Yes | Staff | Approve clearance |
| POST | `/api/approvals/{id}/reject/` | Yes | Staff | Reject clearance |
| PUT | `/api/approvals/{id}/` | Yes | Staff | Update approval |
| GET | `/api/approvals/pending/` | Yes | Staff | Get pending approvals |
| GET | `/api/approvals/by-department/` | Yes | Staff | Get dept's approvals |

---

### Finance Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/finance/payments/` | Yes | Admin | List all payments |
| GET | `/api/finance/my_payment/` | Yes | Student | Get own payment |
| POST | `/api/finance/payments/` | Yes | Admin | Create payment record |
| POST | `/api/finance/payments/{id}/verify/` | Yes | Admin | Verify payment |
| GET | `/api/finance/payments/unverified/` | Yes | Admin | Get unverified payments |
| GET | `/api/finance/payments/statistics/` | Yes | Admin | Payment statistics |
| POST | `/api/finance/mpesa_callback/` | No | Webhook | M-PESA callback |

---

### Department Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/departments/` | Yes | - | List departments |
| POST | `/api/departments/` | Yes | Admin | Create department |
| GET | `/api/departments/{id}/` | Yes | - | Get department |
| PUT | `/api/departments/{id}/` | Yes | Admin | Update department |
| DELETE | `/api/departments/{id}/` | Yes | Admin | Delete department |
| GET | `/api/departments/{id}/approvals/` | Yes | Staff | Get dept approvals |

---

### Notification Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/notifications/` | Yes | User | Get notifications |
| GET | `/api/notifications/{id}/` | Yes | User | Get notification |
| PUT | `/api/notifications/{id}/mark-read/` | Yes | User | Mark as read |
| DELETE | `/api/notifications/{id}/` | Yes | User | Delete notification |
| POST | `/api/notifications/mark-all-read/` | Yes | User | Mark all read |
| GET | `/api/notifications/unread-count/` | Yes | User | Get unread count |

---

### Gown Issuance Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/gown-issuances/` | Yes | Admin | List gown issuances |
| POST | `/api/gown-issuances/` | Yes | Admin | Issue gown |
| GET | `/api/gown-issuances/{id}/` | Yes | - | Get gown details |
| PUT | `/api/gown-issuances/{id}/` | Yes | Admin | Update gown |
| POST | `/api/gown-issuances/{id}/mark-returned/` | Yes | Admin | Mark returned |
| POST | `/api/gown-issuances/{id}/refund-deposit/` | Yes | Admin | Refund deposit |
| GET | `/api/gown-issuances/overdue/` | Yes | Admin | Get overdue returns |
| GET | `/api/gown-issuances/statistics/` | Yes | Admin | Gown statistics |

---

### Audit Log Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/audit-logs/` | Yes | Admin | List audit logs |
| GET | `/api/audit-logs/{id}/` | Yes | Admin | Get log details |
| GET | `/api/audit-logs/statistics/` | Yes | Admin | Log statistics |
| GET | `/api/audit-logs/recent/` | Yes | Admin | Get recent logs |
| GET | `/api/audit-logs/by_user/{user_id}/` | Yes | Admin | Filter by user |

---

### Analytics Endpoints

| Method | Path | Auth | Role | Description |
|--------|------|------|------|-------------|
| GET | `/api/analytics/dashboard/` | Yes | Admin | Dashboard metrics |
| GET | `/api/analytics/completion-rate/` | Yes | Admin | Completion rates |
| GET | `/api/analytics/bottlenecks/` | Yes | Admin | Department bottlenecks |
| GET | `/api/analytics/financial-summary/` | Yes | Admin | Financial summary |
| GET | `/api/analytics/by-cohort/` | Yes | Admin | Stats by cohort |

---

## Data Structures (Request/Response)

### Login Request
```json
{
  "email": "student@mksu.ac.ke",
  "password": "password123"
}
```

### Login Response
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "email": "student@mksu.ac.ke",
    "full_name": "John Doe",
    "role": "student"
  }
}
```

### Clearance Request (Submit)
```json
{
  "student_id": "uuid"
}
```

### Approval Request
```json
{
  "status": "approved",
  "notes": "All fees cleared",
  "evidence_file": "<file_upload>"
}
```

### Payment Verification
```json
{
  "transaction_id": "MPS123456",
  "phone_number": "+254712345678",
  "payment_date": "2024-12-15T12:00:00Z"
}
```

### Error Response
```json
{
  "detail": "Not found",
  "code": "not_found"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No content (delete) |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (no token or expired) |
| 403 | Forbidden (no permission) |
| 404 | Not found |
| 500 | Server error |

### Error Response Format

```json
{
  "detail": "Error message",
  "code": "error_code",
  "field_errors": {
    "email": ["This field is required"]
  }
}
```

---

## Workflow Examples

### Complete Student Clearance Workflow

1. **Student Registers**
   ```
   POST /api/auth/register/
   Body: { email, password, full_name, registration_number }
   Response: { user, tokens }
   ```

2. **Student Logs In**
   ```
   POST /api/auth/token/
   Body: { email, password }
   Response: { access, refresh }
   ```

3. **Student Pays Graduation Fee**
   ```
   POST /api/finance/payments/
   Body: { student_id, amount, payment_method, transaction_id }
   Response: { payment }
   ```

4. **Finance Verifies Payment**
   ```
   POST /api/finance/payments/{id}/verify/
   Body: { verified_by }
   Response: { payment with is_verified=true }
   ```

5. **Student Submits Clearance**
   ```
   POST /api/clearances/
   Body: { student_id }
   Response: { clearance_request with approvals initialized }
   ```

6. **Department Staff Reviews & Approves**
   ```
   POST /api/approvals/{id}/approve/
   Body: { notes, evidence_file }
   Response: { approval with status=approved }
   Trigger: Notification sent to student
   ```

7. **All Departments Approve → Clearance Complete**
   ```
   GET /api/clearances/{id}/
   Response: { status=completed, completion_percentage=100 }
   ```

8. **Gown Issuance**
   ```
   POST /api/gown-issuances/
   Body: { student_id, gown_size, deposit_amount }
   Response: { gown_issuance }
   ```

---

## Security Features

- **JWT Authentication**: Secure token-based auth with refresh tokens
- **RBAC**: Role-based access control at view and serializer level
- **CORS**: Configured for frontend domain only
- **Rate Limiting**: Prevents API abuse
- **Audit Logging**: All sensitive actions logged
- **File Validation**: Evidence files max 5MB, safe formats only
- **Password Security**: Hashing with Django's built-in salt
- **Environment Variables**: All secrets in `.env` file

---

## Rate Limits

- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour
- **Admin endpoints**: 5000 requests/hour

---

## Pagination

Default pagination: 20 items per page  
Query parameter: `?page=1&page_size=50`

---

**End of Document**
