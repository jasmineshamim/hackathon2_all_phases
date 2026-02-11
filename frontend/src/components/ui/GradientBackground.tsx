import React from 'react';

interface GradientBackgroundProps {
  children: React.ReactNode;
  className?: string;
}

export const GradientBackground: React.FC<GradientBackgroundProps> = ({
  children,
  className = '',
}) => {
  return (
    <div className={`min-h-screen bg-auth-gradient flex items-center justify-center p-4 ${className}`}>
      {children}
    </div>
  );
};
