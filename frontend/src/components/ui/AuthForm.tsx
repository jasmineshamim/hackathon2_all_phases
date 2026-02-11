import React from 'react';

interface AuthFormProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  className?: string;
}

export const AuthForm: React.FC<AuthFormProps> = ({
  children,
  title,
  subtitle,
  className = '',
}) => {
  return (
    <div className={`w-full max-w-md ${className}`}>
      <div className="bg-white rounded-2xl shadow-2xl p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {title}
          </h1>
          {subtitle && (
            <p className="text-gray-600">
              {subtitle}
            </p>
          )}
        </div>
        {children}
      </div>
    </div>
  );
};
