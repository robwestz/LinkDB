import React from 'react';

const Header = () => {
  return (
    <header className="bg-white shadow-md">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center">
          <h2 className="text-xl font-semibold text-gray-800">Analytics Dashboard</h2>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-sm text-gray-600">
            <span className="font-medium">LinkDB Analytics</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
