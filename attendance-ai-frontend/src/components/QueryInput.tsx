import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

interface QueryInputProps {
  onGenerate: (query: string) => void;
  isLoading: boolean;
}

export const QueryInput: React.FC<QueryInputProps> = ({ onGenerate, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onGenerate(query.trim());
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <motion.form 
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2, ease: [0.25, 0.1, 0.25, 1] }}
      className="w-full max-w-3xl mx-auto flex flex-col items-center gap-6 mt-8"
    >
      <div className="w-full relative group">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Example: Show attendance of Gangadhar"
          disabled={isLoading}
          className="glass-input w-full min-h-[160px] p-6 text-lg resize-none text-[#1D1D1F] placeholder:text-[#6E6E73]/60 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          autoFocus
        />
        
        {/* Subtle decorative glow effect */}
        <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/0 via-[#007AFF]/5 to-purple-500/0 rounded-[28px] blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none -z-10"></div>
      </div>
      
      <button
        type="submit"
        disabled={!query.trim() || isLoading}
        className="apple-button flex items-center justify-center gap-2 px-8 py-4 text-[17px] min-w-[200px]"
      >
        {isLoading ? (
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 rounded-full border-2 border-white/30 border-t-white animate-spin"></div>
            <span>Generating...</span>
          </div>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            <span>Generate SQL</span>
          </>
        )}
      </button>
    </motion.form>
  );
};
