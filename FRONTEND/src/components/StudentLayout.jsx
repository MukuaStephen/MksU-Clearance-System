import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FileText, Home, DollarSign, ClipboardList, Users } from 'lucide-react';

export default function StudentLayout({ children, student }) {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/payment', label: 'Payment', icon: DollarSign },
    { path: '/application', label: 'Application', icon: FileText },
    { path: '/clearance', label: 'Clearance', icon: ClipboardList }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FileText className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Machakos University</h1>
                <p className="text-sm text-gray-600">Digital Graduation Clearance System</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-600">
                {student?.name || 'Student'} ({student?.regNo || 'N/A'})
              </span>
              <Link 
                to="/admin"
                className="text-sm text-blue-600 hover:text-blue-700"
              >
                Admin Login
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex gap-6">
          <aside className="w-64 flex-shrink-0">
            <div className="bg-white rounded-lg border border-gray-200 p-4 sticky top-24">
              <h3 className="font-semibold text-gray-900 mb-4">Navigation</h3>
              <nav className="space-y-1">
                {navItems.map(item => {
                  const Icon = item.icon;
                  const isActive = location.pathname === item.path;
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                        isActive 
                          ? 'bg-blue-100 text-blue-700 font-medium' 
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      {item.label}
                    </Link>
                  );
                })}
              </nav>
            </div>
          </aside>

          <main className="flex-1">
            {children}
          </main>
        </div>
      </div>

      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>© 2024 Machakos University. All rights reserved.</p>
          <p className="mt-1">For support, contact: registrar@mksu.ac.ke | +254 700 000 000</p>
        </div>
      </footer>
    </div>
  );
}
