import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DollarSign, CreditCard, CheckCircle } from 'lucide-react';

export default function PaymentPage({ student, updateStudent }) {
  const navigate = useNavigate();
  const [mpesaCode, setMpesaCode] = useState('');
  const [amount, setAmount] = useState('5500');

  const handlePayment = (e) => {
    e.preventDefault();
    if (!mpesaCode) {
      alert('Please enter M-PESA confirmation code');
      return;
    }
    
    updateStudent({
      ...student,
      graduationFee: {
        paid: true,
        amount: 5500,
        date: new Date().toISOString().split('T')[0],
        mpesaCode: mpesaCode
      }
    });
    
    alert('Payment recorded successfully!');
    navigate('/application');
  };

  if (student?.graduationFee?.paid) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-start gap-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h3 className="font-semibold text-gray-900 mb-2">Payment Confirmed</h3>
              <div className="text-sm text-gray-600 space-y-1">
                <p>Amount: KES {student.graduationFee.amount.toLocaleString()}</p>
                <p>M-PESA Code: {student.graduationFee.mpesaCode}</p>
                <p>Date: {student.graduationFee.date}</p>
              </div>
            </div>
          </div>
          <button 
            onClick={() => navigate('/application')}
            className="mt-4 w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Continue to Application →
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-6">
          <DollarSign className="w-8 h-8 text-green-600" />
          <div>
            <h2 className="text-xl font-bold text-gray-900">Graduation Fee Payment</h2>
            <p className="text-sm text-gray-600">Step 1 of 3</p>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-gray-900 mb-2">Payment Instructions</h3>
          <ol className="text-sm text-gray-700 space-y-2 list-decimal list-inside">
            <li>Go to M-PESA on your phone</li>
            <li>Select Lipa Na M-PESA → Paybill</li>
            <li>Enter Business Number: <strong>522522</strong></li>
            <li>Account Number: <strong>{student?.regNo || 'Your Registration Number'}</strong></li>
            <li>Amount: <strong>KES 5,500</strong></li>
            <li>Enter your M-PESA PIN and confirm</li>
            <li>Copy the confirmation code below</li>
          </ol>
        </div>

        <form onSubmit={handlePayment} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Amount (KES)
            </label>
            <input
              type="text"
              value={amount}
              disabled
              className="w-full border border-gray-300 rounded-lg px-4 py-2 bg-gray-100"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              M-PESA Confirmation Code *
            </label>
            <input
              type="text"
              value={mpesaCode}
              onChange={(e) => setMpesaCode(e.target.value.toUpperCase())}
              placeholder="e.g., RK45HJ67"
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <p className="text-xs text-gray-500 mt-1">Enter the code from your M-PESA confirmation SMS</p>
          </div>

          <button
            type="submit"
            className="w-full bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors font-medium flex items-center justify-center gap-2"
          >
            <CreditCard className="w-5 h-5" />
            Confirm Payment
          </button>
        </form>
      </div>
    </div>
  );
}
