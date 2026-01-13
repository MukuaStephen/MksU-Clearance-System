# 🚀 Quick Access URLs

## Direct Links to All Sections

### **Student Section** 👨‍🎓
```
Login:      http://localhost:4200/login
Dashboard:  http://localhost:4200/dashboard
Home:       http://localhost:4200/
```

### **Staff Section** 👨‍💼
```
Login:      http://localhost:4200/staff-login
Dashboard:  http://localhost:4200/staff/dashboard
Clearance:  http://localhost:4200/staff/clearance/{id}
```

### **Admin Section** 🔐
```
Login:      http://localhost:4200/admin-login
Dashboard:  http://localhost:4200/admin/dashboard
Users:      http://localhost:4200/admin/user/{id}
```

---

## Backend API Reference

### Health Check
```
GET http://localhost:8000/api/health/
```

### API Documentation
```
Swagger UI:  http://localhost:8000/api/docs/
ReDoc:       http://localhost:8000/api/redoc/
OpenAPI:     http://localhost:8000/api/schema/
Admin:       http://localhost:8000/admin/
```

---

## Quick Copy-Paste URLs

### For Student Portal
```
http://localhost:4200/
```

### For Staff Portal
```
http://localhost:4200/staff-login
```

### For Admin Portal
```
http://localhost:4200/admin-login
```

### For API Docs
```
http://localhost:8000/api/docs/
```

---

## What's Available Now

| Portal | URL | Status |
|--------|-----|--------|
| **Student Login** | /login | ✅ Ready |
| **Student Dashboard** | /dashboard | ✅ Ready |
| **Staff Login** | /staff-login | ✅ Ready |
| **Staff Dashboard** | /staff/dashboard | ✅ Ready |
| **Admin Login** | /admin-login | ✅ Ready |
| **Admin Dashboard** | /admin/dashboard | ✅ Ready |

All UIs are built and styled. Ready for API integration!

---

## How to Start

1. **Backend must be running:**
   ```powershell
   cd BACKEND
   python manage.py runserver 8000
   ```

2. **Frontend must be running:**
   ```powershell
   cd FRONTEND
   npm start
   ```

3. **Open browser and visit URLs above**

---

## Try It Out

### Option 1: Student Flow
1. Open http://localhost:4200/
2. See the login form
3. Click link to go to staff or admin

### Option 2: Staff Flow
1. Open http://localhost:4200/staff-login
2. See staff login form
3. Shows clearance requests table with mock data
4. Can approve/reject (currently shows alerts)

### Option 3: Admin Flow
1. Open http://localhost:4200/admin-login
2. See admin login form
3. Shows system statistics and dashboard
4. Switch between tabs to see different sections

---

## Next: API Integration

Once you connect to backend API, credentials will be:
- **Student:** student@mksu.ac.ke / Student123!
- **Staff:** staff@mksu.ac.ke / Staff123!
- **Admin:** admin@mksu.ac.ke / Admin123!

See `HOW_TO_ACCESS_SECTIONS.md` for full integration guide.
