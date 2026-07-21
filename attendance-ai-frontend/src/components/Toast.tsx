import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, XCircle } from 'lucide-react';

interface ToastProps {
  message: string;
  type: 'success' | 'error';
  isVisible: boolean;
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, type, isVisible, onClose }) => {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 20, scale: 0.95 }}
          transition={{ type: "spring", stiffness: 300, damping: 25 }}
          className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50"
        >
          <div className={`glass-card flex items-center gap-3 px-6 py-3 rounded-full ${type === 'error' ? 'bg-red-500/10 border-red-500/20' : ''}`}>
            {type === 'success' ? (
              <Check className="w-5 h-5 text-green-500" />
            ) : (
              <XCircle className="w-5 h-5 text-red-500" />
            )}
            <span className={`font-medium ${type === 'error' ? 'text-red-600' : 'text-[#1D1D1F]'}`}>
              {message}
            </span>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
