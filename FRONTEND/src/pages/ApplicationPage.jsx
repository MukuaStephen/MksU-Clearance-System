import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Upload, CheckCircle, AlertCircle } from 'lucide-react';

export default function ApplicationPage({ student, updateStudent }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: student?.name || '',
    regNo: student?.regNo || '',
    course: student?.course || '',
    email: student?.email || '',
    phone: student?.phone || ''
  });
  const [uploadedFile, setUploadedFile] = useState(null);

  if (!student?.graduationFee?.paid) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <AlertCircle className="w-6 h-6 text-yellow-600 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Payment Required</h3>
              <p className="text-gray-700 mb-4">You must complete the graduation fee payment before submitting your application.</p>
              <button 
                onClick={() => navigate('/payment')}
                className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition-colors"
              >
                Go to Payment
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    
    updateStudent({
      ...student,
      ...formData,
      applicationSubmitted: true,
      applicationDate: new Date().toISOString().split('T')[0]
    });
    
    alert('Application submitted successfully! Finance will now verify your payment.');
    navigate('/clearance');
  };

  if (student?.applicationSubmitted) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-start gap-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Application Submitted</h3>
              <p className="text-gray-700 mb-1">Your graduation application has been received.</p>
              <p className="text-sm text-gray-600">Submitted on: {student.applicationDate}</p>
            </div>
          </div>
          <button 
            onClick={() => navigate('/clearance')}
            className="mt-4 w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Continue to Clearance →
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-6">
          <FileText className="w-8 h-8 text-blue-600" />
          <div>
            <h2 className="text-xl font-bold text-gray-900">Graduation Application Form</h2>
            <p className="text-sm text-gray-600">Step 2 of 3</p>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-gray-700">
            Fill in your details below. After submission, the system will automatically route your application to Finance for verification, then to your Faculty for academic clearance.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name *
            </label>
            <input
              type="text"
              value={formData.fullName}
              onChange={(e) => setFormData({...formData, fullName: e.target.value})}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Registration Number *
              </label>
              <input
                type="text"
                value={formData.regNo}
                onChange={(e) => setFormData({...formData, regNo: e.target.value})}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Course *
              </label>
              <input
                type="text"
                value={formData.course}
                onChange={(e) => setFormData({...formData, course: e.target.value})}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address *
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number *
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Signed Form (Optional)
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <input
                type="file"
                onChange={(e) => setUploadedFile(e.target.files[0])}
                className="hidden"
                id="file-upload"
                accept=".pdf,.jpg,.jpeg,.png"
              />
              <label htmlFor="file-upload" className="cursor-pointer text-blue-600 hover:text-blue-700">
                Click to upload
              </label>
              <p className="text-xs text-gray-500 mt-1">PDF, JPG, or PNG (Max 5MB)</p>
              {uploadedFile && <p className="text-sm text-green-600 mt-2">✓ {uploadedFile.name}</p>}
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Submit Application
          </button>
        </form>
      </div>
    </div>
  );
}
