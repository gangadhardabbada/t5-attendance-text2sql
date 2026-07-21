import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Download, Check } from 'lucide-react';

interface SQLViewerProps {
  sql: string;
  onClear: () => void;
  onCopySuccess: () => void;
}

export const SQLViewer: React.FC<SQLViewerProps> = ({ sql, onClear, onCopySuccess }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    onCopySuccess();
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([sql], { type: 'text/sql' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'query.sql';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 200, damping: 20 }}
      className="glass-card mt-8 w-full max-w-3xl mx-auto overflow-hidden"
    >
      <div className="flex items-center justify-between px-6 py-4 border-b border-white/20 bg-white/40">
        <h3 className="font-semibold text-[#1D1D1F]">Generated SQL</h3>
        <div className="flex items-center gap-2">
          <button 
            onClick={handleCopy}
            className="p-2 hover:bg-black/5 rounded-lg transition-colors text-[#6E6E73] hover:text-[#1D1D1F]"
            title="Copy SQL"
          >
            {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
          </button>
          <button 
            onClick={handleDownload}
            className="p-2 hover:bg-black/5 rounded-lg transition-colors text-[#6E6E73] hover:text-[#1D1D1F]"
            title="Download SQL"
          >
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>
      
      <div className="p-4 bg-[#1E1E1E]">
        <SyntaxHighlighter 
          language="sql" 
          style={vscDarkPlus}
          customStyle={{
            background: 'transparent',
            padding: 0,
            margin: 0,
            fontSize: '14px',
            fontFamily: 'var(--font-mono)'
          }}
          wrapLines={true}
          wrapLongLines={true}
        >
          {sql}
        </SyntaxHighlighter>
      </div>
      
      <div className="px-6 py-4 bg-white/40 border-t border-white/20 flex justify-end">
        <button 
          onClick={onClear}
          className="text-sm font-medium text-[#6E6E73] hover:text-[#1D1D1F] transition-colors"
        >
          Clear Result
        </button>
      </div>
    </motion.div>
  );
};
