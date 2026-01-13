# 🧪 API Integration Testing Guide

## ✅ Everything is Now Connected!

The frontend is **fully integrated** with the backend. Here's how to test it.

---

## 🚀 Quick Start

### Terminal 1: Start Backend
```powershell
cd BACKEND
python manage.py runserver 8000
```

### Terminal 2: Start Frontend
```powershell
cd FRONTEND
npm start
```

---

## 🧑‍🎓 Test 1: Student Registration & Login

### Register New Student
1. Open http://localhost:4200/
2. Click "Register here"
3. Fill in:
   - Full Name: Your Name
   - Admission Number: SCE/CS/0001/2024
   - Email: student@mksu.ac.ke
   - Password: Student123!
   - Confirm Password: Student123!
4. Click Register
5. ✅ Should auto-login and show Student Dashboard

### Alternative: Direct Login
1. If registration fails, try logging in with any credentials
2. Backend will tell you which credentials are valid
3. Check error message for details

---

## 👨‍💼 Test 2: Staff Portal

### Staff Login
1. Go to http://localhost:4200/staff-login
2. Enter staff credentials:
   - Email: staff@mksu.ac.ke
   - Password: Staff123!
3. Click Login
4. ✅ Should redirect to Staff Dashboard

### What You'll See
- Table of clearance requests (if any exist)
- Filter by Status dropdown
- Approve/Reject buttons for each request

### Test Approve/Reject
1. Find a pending clearance
2. Click "Approve" button
3. ✅ Should show success message and refresh the list

---

## 🔐 Test 3: Admin Portal

### Admin Login
1. Go to http://localhost:4200/admin-login
2. Enter admin credentials:
   - Email: admin@mksu.ac.ke
   - Password: Admin123!
3. Click Login
4. ✅ Should redirect to Admin Dashboard

### What You'll See
- System statistics (Total Students, Staff, etc.)
- Tabs: Dashboard, Users Management, Settings
- Real data from the database

### Test Users Tab
1. Click on "Users Management" tab
2. ✅ Should show list of students from database
3. Try deleting a user (optional)

---

## 🔍 Browser DevTools Debugging

### Check Network Requests
1. Open http://localhost:4200/
2. Press F12 to open DevTools
3. Go to "Network" tab
4. Login with any credentials
5. Look for requests to:
   - `http://localhost:8000/api/auth/login/`
   - Check response contains `access` token
   - Check `Authorization` header in subsequent requests

### Check LocalStorage
1. Press F12
2. Go to "Application" tab
3. Expand "Local Storage"
4. Click "localhost:4200"
5. ✅ Should see:
   - `access_token`
   - `refresh_token`
   - `user_role`
   - `user_id`
   - `user_email`

### Check Console Errors
1. Press F12
2. Go to "Console" tab
3. Should see minimal errors
4. If you see CORS errors, check backend settings

---

## 🐛 Troubleshooting

### "Cannot connect to server"
**Problem:** Frontend can't reach backend
**Solution:**
1. Check backend is running: `python manage.py runserver 8000`
2. Test manually: `curl http://localhost:8000/api/health/`
3. Check no firewall blocking port 8000

### "Invalid email or password"
**Problem:** Login credentials don't match
**Solution:**
1. Backend doesn't have that user account
2. Create user first or use correct credentials
3. Check database has users (sqlite3 or MySQL)

### "You must be admin to access this portal"
**Problem:** Logged in with non-admin account to admin portal
**Solution:**
1. Use admin account credentials
2. Or login to student/staff portal instead

### Network request shows 401 Unauthorized
**Problem:** Token expired or invalid
**Solution:**
1. The access token may have expired
2. Logout and login again
3. Check `access_token` in localStorage isn't corrupt

### Form won't submit
**Problem:** Form validation error
**Solution:**
1. Check all required fields are filled
2. Look for red error messages
3. Check browser console for JavaScript errors

---

## 📊 Testing Checklist

- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:4200
- [ ] Student registration works
- [ ] Student login works
- [ ] Student dashboard shows (even with no data)
- [ ] Staff login works
- [ ] Staff dashboard loads clearances
- [ ] Staff can approve clearances
- [ ] Admin login works
- [ ] Admin dashboard shows statistics
- [ ] Admin users management loads students
- [ ] No CORS errors in browser console
- [ ] Tokens stored in localStorage after login
- [ ] Logout clears localStorage

---

## 🔄 API Response Examples

### Successful Login Response
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "student@mksu.ac.ke",
    "full_name": "Student Name",
    "role": "student"
  }
}
```

### Clearance List Response
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "student": 1,
      "status": "pending",
      "submitted_date": "2025-01-13T10:00:00Z",
      ...
    }
  ]
}
```

### Error Response
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 🎯 Test Scenarios

### Scenario 1: Full Student Workflow
1. Register new student account ✅
2. Auto-login to dashboard ✅
3. View clearance status ✅
4. Logout ✅

### Scenario 2: Staff Workflow
1. Login as staff ✅
2. View clearance requests ✅
3. Approve a request ✅
4. See updated status ✅
5. Logout ✅

### Scenario 3: Admin Workflow
1. Login as admin ✅
2. View dashboard stats ✅
3. Go to users management ✅
4. View user list from database ✅
5. (Optional) Delete a user ✅
6. Logout ✅

---

## 📝 Notes

- **Tokens expire after:** Check settings.py for JWT_ACCESS_TOKEN_LIFETIME
- **Database:** SQLite (db.sqlite3) or MySQL depending on configuration
- **CORS:** Enabled for http://localhost:4200 in backend settings
- **Authentication:** JWT (JSON Web Tokens)
- **Password Storage:** Hashed with Django's default hasher

---

## 🎉 Success Indicators

✅ **Login works without errors**
✅ **Tokens appear in localStorage**
✅ **Dashboard loads real data from backend**
✅ **API requests visible in Network tab**
✅ **No CORS or 401 errors**
✅ **Logout clears session**

**If all checkmarks pass, your integration is working correctly!**

---

## 📞 Need Help?

If something doesn't work:
1. Check the error message in the browser
2. Look at the Network tab to see the API response
3. Check browser Console for JavaScript errors
4. Verify backend is running and responding
5. Check user exists in database
6. See API_INTEGRATION_COMPLETE.md for more details
