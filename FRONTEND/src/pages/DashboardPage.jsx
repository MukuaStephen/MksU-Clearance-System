import React from 'react';
import { useNavigate } from 'react-router-dom';
import { CheckCircle, Clock, AlertCircle, ArrowRight } from 'lucide-react';

export default function DashboardPage({ student }) {
  const navigate = useNavigate();

  const getProgressPercentage = () => {
    if (!student?.clearances) return 0;
    const total = Object.keys(student.clearances).length;
    const approved = Object.values(student.clearances).filter(c => c.status === 'approved').length;
    return Math.round((approved / total) * 100);
  };

  const progress = getProgressPercentage();

  const steps = [
    {
      id: 1,
      title: 'Payment',
      description: 'Pay KES 5,500 graduation fee',
      completed: student?.graduationFee?.paid,
      path: '/payment'
    },
    {
      id: 2,
      title: 'Application',
      description: 'Submit graduation application form',
      completed: student?.applicationSubmitted,
      path: '/application'
    },
    {
      id: 3,
      title: 'Clearance',
      description: 'Get cleared by all departments',
      completed: progress === 100,
      path: '/clearance'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg p-6 text-white">
        <h2 className="text-2xl font-bold mb-2">Welcome, {student?.name || 'Student'}!</h2>
        <p className="text-blue-100">Track your graduation clearance progress below</p>
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div><span className="text-blue-200">Reg No:</span> <span className="font-semibold">{student?.regNo || 'N/A'}</span></div>
          <div><span className="text-blue-200">Course:</span> <span className="font-semibold">{student?.course || 'N/A'}</span></div>
          <div><span className="text-blue-200">Email:</span> <span className="font-semibold">{student?.email || 'N/A'}</span></div>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Clearance Steps</h3>
        <div className="space-y-4">
          {steps.map((step, index) => (
            <div key={step.id} className="relative">
              {index < steps.length - 1 && (
                <div className="absolute left-6 top-12 bottom-0 w-0.5 bg-gray-200" />
              )}
              <div className="flex items-start gap-4 relative">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${
                  step.completed ? 'bg-green-100' : 'bg-gray-100'
                }`}>
                  {step.completed ? (
                    <CheckCircle className="w-6 h-6 text-green-600" />
                  ) : (
                    <Clock className="w-6 h-6 text-gray-400" />
                  )}
                </div>
                <div className="flex-1 pt-2">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="font-semibold text-gray-900">{step.title}</h4>
                      <p className="text-sm text-gray-600">{step.description}</p>
                    </div>
                    {!step.completed && (
                      <button
                        onClick={() => navigate(step.path)}
                        className="text-blue-600 hover:text-blue-700 flex items-center gap-1 text-sm font-medium"
                      >
                        Start <ArrowRight className="w-4 h-4" />
                      </button>
                    )}
                    {step.completed && (
                      <span className="text-green-600 text-sm font-medium">Completed</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {student?.graduationFee?.paid && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="font-semibold text-gray-900 mb-3">Payment Details</h3>
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

      {progress === 100 && (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <CheckCircle className="w-8 h-8 text-green-600 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-bold text-green-900 mb-2">🎓 Ready for Graduation!</h3>
              <p className="text-green-800 mb-4">Congratulations! You have completed all clearance requirements.</p>
              <button className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium">
                Download Clearance Certificate
              </button>
            </div>
          </div>
        </div>
      )}

      {student?.overallStatus === 'blocked' && (
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <AlertCircle className="w-8 h-8 text-red-600 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-bold text-red-900 mb-2">Action Required</h3>
              <p className="text-red-800 mb-4">Some departments have flagged issues. Please visit the Clearance page to see details.</p>
              <button 
                onClick={() => navigate('/clearance')}
                className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors font-medium"
              >
                View Clearance Details
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
