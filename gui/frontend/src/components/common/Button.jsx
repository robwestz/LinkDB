import React from 'react';

const Button = ({ children, onClick, variant = 'primary', className = '', ...props }) => {
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  };

  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
        variantClasses[variant] || variantClasses.primary
      } ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
