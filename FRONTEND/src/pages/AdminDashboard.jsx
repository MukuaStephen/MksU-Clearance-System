import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { CheckCircle, XCircle, Clock, Users, FileText, BookOpen, Home, DollarSign, Utensils } from 'lucide-react';

export default function AdminDashboard({ student, updateStudent }) {
  const [selectedDept, setSelectedDept] = useState('');
  const [notes, setNotes] = useState('');
  const [students, setStudents] = useState([]);

  useEffect(() => {
    // Load all students from localStorage or generate sample
    try {
      const stored = localStorage.getItem('all-students-data');
      if (stored) {
        setStudents(JSON.parse(stored));
      } else {
        const sampleStudents = generateSampleStudents();
        setStudents(sampleStudents);
        localStorage.setItem('all-students-data', JSON.stringify(sampleStudents));
      }
    } catch (error) {
      const sampleStudents = generateSampleStudents();
      setStudents(sampleStudents);
    }
  }, []);

  const generateSampleStudents = () => {
    return [
      {
        id: 'STU001',
        name: 'John Kamau',
        regNo: 'CS/2020/001',
        course: 'BSc Computer Science',
        email: 'john.kamau@student.mksu.ac.ke',
        phone: '+254712345678',
        graduationFee: { paid: true, amount: 5500, date: '2024-11-15', mpesaCode: 'RK45HJ67' },
        applicationSubmitted: true,
        applicationDate: '2024-11-15',
        clearances: {
          finance: { status: 'approved', approvedBy: 'Jane Mwangi', date: '2024-11-16', notes: 'All fees paid' },
          faculty: { status: 'approved', approvedBy: 'Dr. Peter Omondi', date: '2024-11-17', notes: 'Cleared' },
          library: { status: 'pending', approvedBy: null, date: null, notes: null },
          mess: { status: 'pending', approvedBy: null, date: null, notes: null },
          hostel: { status: 'pending', approvedBy: null, date: null, notes: null }
        },
        overallStatus: 'in-progress'
      },
      {
        id: 'STU002',
        name: 'Mary Wanjiku',
        regNo: 'BA/2020/045',
        course: 'BA Business Administration',
        email: 'mary.wanjiku@student.mksu.ac.ke',
        phone: '+254723456789',
        graduationFee: { paid: true, amount: 5500, date: '2024-11-14', mpesaCode: 'TY67KL89' },
        applicationSubmitted: true,
        applicationDate: '2024-11-14',
        clearances: {
          finance: { status: 'approved', approvedBy: 'Jane Mwangi', date: '2024-11-15', notes: 'All fees paid' },
          faculty: { status: 'approved', approvedBy: 'Prof. Sarah Kimani', date: '2024-11-16', notes: 'Cleared' },
          library: { status: 'approved', approvedBy: 'James Muthoni', date: '2024-11-17', notes: 'No pending books' },
          mess: { status: 'approved', approvedBy: 'Grace Njeri', date: '2024-11-17', notes: 'No dues' },
          hostel: { status: 'pending', approvedBy: null, date: null, notes: null }
        },
        overallStatus: 'in-progress'
      }
    ];
  };

  const departments = [
    { id: 'finance', name: 'Finance Office', icon: DollarSign },
    { id: 'faculty', name: 'Faculty Office', icon: Users },
    { id: 'library', name: 'Library', icon: BookOpen },
    { id: 'mess', name: 'Mess/Cafeteria', icon: Utensils },
    { id: 'hostel', name: 'Hostel', icon: Home }
  ];

  const getStatusBadge = (status) => {
    const styles = {
      approved: 'bg-green-100 text-green-800 border-green-200',
      pending: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      rejected: 'bg-red-100 text-red-800 border-red-200'
    };
    const icons = {
      approved: <CheckCircle className="w-4 h-4" />,
      pending: <Clock className="w-4 h-4" />,
      rejected: <XCircle className="w-4 h-4" />
    };
    return (
      <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium border ${styles[status]}`}>
        {icons[status]}
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const handleApproval = (studentId, dept, action) => {
    const updatedStudents = students.map(s => {
      if (s.id === studentId) {
        const newClearances = { ...s.clearances };
        newClearances[dept] = {
          status: action,
          approvedBy: `${departments.find(d => d.id === dept)?.name} Admin`,
          date: new Date().toISOString().split('T')[0],
          notes: notes || (action === 'approved' ? 'Cleared' : 'Rejected')
        };
        
        const allApproved = Object.values(newClearances).every(c => c.status === 'approved');
        const hasRejection = Object.values(newClearances).some(c => c.status === 'rejected');
        
        return {
          ...s,
          clearances: newClearances,
          overallStatus: hasRejection ? 'blocked' : allApproved ? 'completed' : 'in-progress'
        };
      }
      return s;
    });
    
    setStudents(updatedStudents);
    localStorage.setItem('all-students-data', JSON.stringify(updatedStudents));
    setNotes('');
    alert(`${action === 'approved' ? 'Approved' : 'Rejected'} clearance for ${departments.find(d => d.id === dept)?.name}`);
  };

  const getProgressPercentage = (student) => {
    const total = Object.keys(student.clearances).length;
    const approved = Object.values(student.clearances).filter(c => c.status === 'approved').length;
    return Math.round((approved / total) * 100);
  };

  const [selectedStudent, setSelectedStudent] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');

  const filteredStudents = students.filter(s => {
    if (filterStatus === 'all') return true;
    if (filterStatus === 'pending') return Object.values(s.clearances).some(c => c.status === 'pending');
    if (filterStatus === 'completed') return s.overallStatus === 'completed';
    return true;
  });

  if (selectedStudent) {
    const student = students.find(s => s.id === selectedStudent.id);
    if (!student) {
      setSelectedStudent(null);
      return null;
    }

    return (
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <FileText className="w-8 h-8 text-purple-600" />
                <div>
                  <h1 className="text-xl font-bold text-gray-900">Student Details</h1>
                  <p className="text-sm text-gray-600">{student.name}</p>
                </div>
              </div>
              <div className="flex gap-3">
                <button 
                  onClick={() => setSelectedStudent(null)}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  ← Back to Student List
                </button>
                <Link to="/" className="text-sm text-gray-600 hover:text-gray-700">
                  Student Portal
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-4xl mx-auto px-4 py-6 space-y-6">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Student Information</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Full Name:</span>
                <p className="font-medium text-gray-900">{student.name}</p>
              </div>
              <div>
                <span className="text-gray-600">Registration No:</span>
                <p className="font-medium text-gray-900">{student.regNo}</p>
              </div>
              <div>
                <span className="text-gray-600">Course:</span>
                <p className="font-medium text-gray-900">{student.course}</p>
              </div>
              <div>
                <span className="text-gray-600">Email:</span>
                <p className="font-medium text-gray-900">{student.email}</p>
              </div>
              <div>
                <span className="text-gray-600">Phone:</span>
                <p className="font-medium text-gray-900">{student.phone}</p>
              </div>
              <div>
                <span className="text-gray-600">Application Status:</span>
                <p className="font-medium text-gray-900">{student.applicationSubmitted ? `Submitted (${student.applicationDate})` : 'Not Submitted'}</p>
              </div>
            </div>
          </div>

          {student.graduationFee?.paid && (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="font-semibold text-gray-900 mb-3">Payment Information</h3>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <div className="text-sm text-gray-700 space-y-1">
                    <p>Amount: <strong>KES {student.graduationFee.amount?.toLocaleString()}</strong></p>
                    <p>M-PESA Code: <strong>{student.graduationFee.mpesaCode}</strong></p>
                    <p>Date: <strong>{student.graduationFee.date}</strong></p>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Department Clearances</h3>
            <p className="text-sm text-gray-600 mb-4">Select a department clearance to approve or reject</p>
            
            <div className="space-y-4">
              {departments.map(dept => {
                const clearance = student.clearances[dept.id];
                const Icon = dept.icon;
                return (
                  <div key={dept.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <Icon className="w-6 h-6 text-gray-600" />
                        <div>
                          <h4 className="font-medium text-gray-900">{dept.name}</h4>
                          {clearance.status !== 'pending' && clearance.approvedBy && (
                            <p className="text-sm text-gray-600 mt-1">
                              Processed by: {clearance.approvedBy} on {clearance.date}
                            </p>
                          )}
                          {clearance.notes && (
                            <p className="text-sm text-gray-600 italic mt-1">Notes: {clearance.notes}</p>
                          )}
                        </div>
                      </div>
                      {getStatusBadge(clearance.status)}
                    </div>

                    {clearance.status === 'pending' && (
                      <div className="mt-4 bg-gray-50 p-4 rounded-lg space-y-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Notes (optional)
                          </label>
                          <textarea
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                            placeholder="Add any notes or comments..."
                            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            rows="2"
                          />
                        </div>
                        <div className="flex gap-3">
                          <button
                            onClick={() => {
                              handleApproval(student.id, dept.id, 'approved');
                              const updatedStudent = students.find(s => s.id === student.id);
                              setSelectedStudent(updatedStudent);
                            }}
                            className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium text-sm"
                          >
                            Approve {dept.name}
                          </button>
                          <button
                            onClick={() => {
                              handleApproval(student.id, dept.id, 'rejected');
                              const updatedStudent = students.find(s => s.id === student.id);
                              setSelectedStudent(updatedStudent);
                            }}
                            className="flex-1 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors font-medium text-sm"
                          >
                            Reject {dept.name}
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-semibold text-gray-900">Overall Progress</h4>
                <p className="text-sm text-gray-600">{getProgressPercentage(student)}% Complete</p>
              </div>
              <button 
                onClick={() => setSelectedStudent(null)}
                className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
              >
                Done
              </button>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FileText className="w-8 h-8 text-purple-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Admin Panel</h1>
                <p className="text-sm text-gray-600">Graduation Clearance Management</p>
              </div>
            </div>
            <Link to="/" className="text-sm text-blue-600 hover:text-blue-700">
              ← Back to Student Portal
            </Link>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="bg-gradient-to-r from-purple-600 to-purple-800 rounded-lg p-6 text-white mb-6">
          <h2 className="text-2xl font-bold mb-2">Department Clearance Control</h2>
          <p className="text-purple-100">Select a student to review and process clearances</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <p className="text-sm text-gray-600 mb-1">Total Students</p>
            <p className="text-3xl font-bold text-gray-900">{students.length}</p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <p className="text-sm text-gray-600 mb-1">Pending Clearances</p>
            <p className="text-3xl font-bold text-yellow-600">
              {students.reduce((acc, s) => acc + Object.values(s.clearances).filter(c => c.status === 'pending').length, 0)}
            </p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <p className="text-sm text-gray-600 mb-1">Fully Cleared</p>
            <p className="text-3xl font-bold text-green-600">
              {students.filter(s => s.overallStatus === 'completed').length}
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Student List</h3>
            <select 
              className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="all">All Students</option>
              <option value="pending">With Pending Clearances</option>
              <option value="completed">Fully Cleared</option>
            </select>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Student</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Reg No</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Course</th>
                  <th className="px-4 py-3 text-center text-sm font-semibold text-gray-900">Progress</th>
                  <th className="px-4 py-3 text-center text-sm font-semibold text-gray-900">Status</th>
                  <th className="px-4 py-3 text-center text-sm font-semibold text-gray-900">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredStudents.map(s => {
                  const progress = getProgressPercentage(s);
                  const pendingCount = Object.values(s.clearances).filter(c => c.status === 'pending').length;
                  return (
                    <tr key={s.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <div>
                          <p className="text-sm font-medium text-gray-900">{s.name}</p>
                          <p className="text-xs text-gray-500">{s.email}</p>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600">{s.regNo}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{s.course}</td>
                      <td className="px-4 py-3">
                        <div className="flex flex-col items-center gap-1">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${progress}%` }}></div>
                          </div>
                          <span className="text-xs font-medium text-gray-700">{progress}%</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${
                          s.overallStatus === 'completed' ? 'bg-green-100 text-green-800' :
                          s.overallStatus === 'blocked' ? 'bg-red-100 text-red-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {pendingCount > 0 ? `${pendingCount} pending` : s.overallStatus}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <button
                          onClick={() => setSelectedStudent(s)}
                          className="text-purple-600 hover:text-purple-800 font-medium text-sm hover:underline"
                        >
                          View Details →
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {filteredStudents.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <p>No students found matching the selected filter.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
