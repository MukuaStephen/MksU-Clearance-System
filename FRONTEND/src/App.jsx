import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import StudentLayout from './components/StudentLayout';
import DashboardPage from './pages/DashboardPage';
import PaymentPage from './pages/PaymentPage';
import ApplicationPage from './pages/ApplicationPage';
import ClearancePage from './pages/ClearancePage';
import AdminDashboard from './pages/AdminDashboard';

const App = () => {
  const [student, setStudent] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = () => {
    try {
      const stored = localStorage.getItem('student-data');
      if (stored) {
        setStudent(JSON.parse(stored));
      } else {
        const initialStudent = {
          id: 'STU001',
          name: 'John Kamau',
          regNo: 'CS/2020/001',
          course: 'BSc Computer Science',
          email: 'john.kamau@student.mksu.ac.ke',
          phone: '+254712345678',
          graduationFee: { paid: true, amount: 5500, date: '2024-12-01', mpesaCode: 'RK45HJ67' },
          applicationSubmitted: true,
          applicationDate: '2024-12-02',
          clearances: {
            finance: { status: 'approved', approvedBy: 'Jane Mwangi', date: '2024-12-03', notes: 'All fees verified and cleared' },
            faculty: { status: 'approved', approvedBy: 'Dr. Peter Omondi', date: '2024-12-04', notes: 'Academic requirements met' },
            library: { status: 'pending', approvedBy: null, date: null, notes: null },
            mess: { status: 'pending', approvedBy: null, date: null, notes: null },
            hostel: { status: 'pending', approvedBy: null, date: null, notes: null }
          },
          overallStatus: 'in-progress'
        };
        setStudent(initialStudent);
        saveData(initialStudent);
      }
    } catch (error) {
      console.error('Load error:', error);
    }
  };

  const saveData = (studentData) => {
    try {
      localStorage.setItem('student-data', JSON.stringify(studentData));
    } catch (error) {
      console.error('Save error:', error);
    }
  };

  const updateStudent = (updatedStudent) => {
    setStudent(updatedStudent);
    saveData(updatedStudent);
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/admin" element={<AdminDashboard student={student} updateStudent={updateStudent} />} />
        <Route path="/*" element={
          <StudentLayout student={student}>
            <Routes>
              <Route path="/" element={<DashboardPage student={student} />} />
              <Route path="/payment" element={<PaymentPage student={student} updateStudent={updateStudent} />} />
              <Route path="/application" element={<ApplicationPage student={student} updateStudent={updateStudent} />} />
              <Route path="/clearance" element={<ClearancePage student={student} updateStudent={updateStudent} />} />
            </Routes>
          </StudentLayout>
        } />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
