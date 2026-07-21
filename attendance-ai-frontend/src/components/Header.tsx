import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="flex justify-between items-center py-6 px-8 max-w-[900px] mx-auto w-full">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-500 to-indigo-500 shadow-sm flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
          </svg>
        </div>
        <span className="font-semibold text-lg tracking-tight text-[#1D1D1F]">T5 Attendance</span>
      </div>
      
      <div className="flex items-center gap-2 px-3 py-1.5 bg-white/60 backdrop-blur-md rounded-full border border-white/80 shadow-sm">
        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
        <span className="text-xs font-medium text-[#6E6E73]">Local Model</span>
      </div>
    </header>
  );
};
