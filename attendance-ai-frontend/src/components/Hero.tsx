import React from 'react';
import { motion } from 'framer-motion';

export const Hero: React.FC = () => {
  return (
    <div className="text-center py-12 px-4">
      <motion.h1 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.25, 0.1, 0.25, 1] }}
        className="text-4xl md:text-5xl font-bold tracking-tight text-[#1D1D1F] mb-4"
      >
        Attendance Text-to-SQL
      </motion.h1>
      <motion.p 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1, ease: [0.25, 0.1, 0.25, 1] }}
        className="text-lg md:text-xl text-[#6E6E73] max-w-2xl mx-auto"
      >
        Convert natural language into SQL queries using a locally fine-tuned T5-Small model.
      </motion.p>
    </div>
  );
};
