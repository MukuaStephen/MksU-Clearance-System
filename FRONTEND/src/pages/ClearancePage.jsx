import React from 'react';
import { useNavigate } from 'react-router-dom';
import { CheckCircle, Clock, XCircle, AlertCircle, BookOpen, Home, DollarSign, Utensils, Users } from 'lucide-react';

export default function ClearancePage({ student, updateStudent }) {
  const navigate = useNavigate();

  const departments = [
    { id: 'finance', name: 'Finance Office', icon: DollarSign, color: 'green' },
    { id: 'faculty', name: 'Faculty Office', icon: Users, color: 'blue' },
    { id: 'library', name: 'Library', icon: BookOpen, color: 'purple' },
    { id: 'mess', name: 'Mess/Cafeteria', icon: Utensils, color: 'orange' },
    { id: 'hostel', name: 'Hostel', icon: Home, color: 'indigo' }
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

  const getProgressPercentage = () => {
    if (!student?.clearances) return 0;
    const total = Object.keys(student.clearances).length;
    const approved = Object.values(student.clearances).filter(c => c.status === 'approved').length;
    return Math.round((approved / total) * 100);
  };

  if (!student?.applicationSubmitted) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <AlertCircle className="w-6 h-6 text-yellow-600 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Application Required</h3>
              <p className="text-gray-700 mb-4">You must submit your graduation application before starting the clearance process.</p>
              <button 
                onClick={() => navigate('/application')}
                className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition-colors"
              >
                Go to Application
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const progress = getProgressPercentage();
  const allCleared = progress === 100;
  const hasRejection = student?.clearances && Object.values(student.clearances).some(c => c.status === 'rejected');

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <BookOpen className="w-8 h-8 text-blue-600" />
          <div>
            <h2 className="text-xl font-bold text-gray-900">Department Clearances</h2>
            <p className="text-sm text-gray-600">Step 3 of 3</p>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-4 mb-6">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-lg font-semibold text-gray-900">Overall Progress</h3>
            <span className="text-2xl font-bold text-blue-600">{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div className="bg-blue-600 h-3 rounded-full transition-all duration-500" style={{ width: `${progress}%` }}></div>
          </div>
          <p className="mt-2 text-sm text-gray-600">
            {allCleared ? 'All clearances completed!' : 
             `${Object.values(student.clearances).filter(c => c.status === 'approved').length} of ${Object.keys(student.clearances).length} departments cleared`}
          </p>
        </div>

        <div className="space-y-4">
          {departments.map(dept => {
            const clearance = student.clearances[dept.id];
            const Icon = dept.icon;
            return (
              <div key={dept.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-1">
                    <div className={`p-2 bg-${dept.color}-100 rounded-lg`}>
                      <Icon className={`w-5 h-5 text-${dept.color}-600`} />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-900">{dept.name}</h4>
                      {clearance.status !== 'pending' && (
                        <div className="mt-2 text-sm text-gray-600 space-y-1">
                          <p>Processed by: {clearance.approvedBy}</p>
                          <p>Date: {clearance.date}</p>
                          {clearance.notes && <p className="italic">Notes: {clearance.notes}</p>}
                        </div>
                      )}
                      {clearance.status === 'pending' && (
                        <p className="mt-1 text-sm text-gray-500">Awaiting verification from {dept.name}</p>
                      )}
                    </div>
                  </div>
                  <div>{getStatusBadge(clearance.status)}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {allCleared && (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <CheckCircle className="w-8 h-8 text-green-600 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-bold text-green-900 mb-2">Clearance Completed!</h3>
              <p className="text-green-800 mb-4">Congratulations! All departments have cleared you for graduation. You may now collect your graduation gown.</p>
              <button className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium">
                Download Clearance Certificate
              </button>
            </div>
          </div>
        </div>
      )}

      {hasRejection && (
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <AlertCircle className="w-8 h-8 text-red-600 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-bold text-red-900 mb-2">Action Required</h3>
              <p className="text-red-800">One or more departments have flagged issues. Please resolve the outstanding matters before proceeding.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
