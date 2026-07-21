import React from 'react';
import { motion } from 'framer-motion';

export const Footer: React.FC = () => {
  return (
    <motion.footer 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.5, duration: 0.8 }}
      className="max-w-[900px] mx-auto w-full mt-16 mb-8 px-4"
    >
      <div className="glass-card flex flex-wrap justify-center gap-x-8 gap-y-4 py-4 px-6 text-sm text-[#6E6E73]">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-[#1D1D1F]">Model:</span>
          <span>T5-Small</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="font-semibold text-[#1D1D1F]">Backend:</span>
          <span>FastAPI</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="font-semibold text-[#1D1D1F]">Database:</span>
          <span>PostgreSQL</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="font-semibold text-[#1D1D1F]">Inference:</span>
          <span>Local</span>
        </div>
      </div>
    </motion.footer>
  );
};
