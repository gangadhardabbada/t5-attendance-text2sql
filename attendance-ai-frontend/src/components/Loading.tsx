import React from 'react';
import { motion } from 'framer-motion';

export const Loading: React.FC = () => {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.3 }}
      className="glass-card p-6 mt-8 w-full max-w-3xl mx-auto overflow-hidden relative"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="w-5 h-5 rounded-full border-2 border-[#007AFF] border-t-transparent animate-spin"></div>
        <h3 className="font-semibold text-[#1D1D1F]">Generating SQL...</h3>
      </div>
      
      <div className="space-y-3">
        <div className="h-4 bg-black/5 rounded w-3/4 shimmer"></div>
        <div className="h-4 bg-black/5 rounded w-1/2 shimmer"></div>
        <div className="h-4 bg-black/5 rounded w-5/6 shimmer"></div>
      </div>
      
      {/* Apple Intelligence style blurred blobs in background */}
      <div className="absolute top-[-50%] left-[-20%] w-[150%] h-[200%] bg-gradient-to-r from-blue-400/20 via-purple-400/20 to-indigo-400/20 blur-3xl rounded-full opacity-50 animate-pulse pointer-events-none" style={{ animationDuration: '4s' }}></div>
    </motion.div>
  );
};
