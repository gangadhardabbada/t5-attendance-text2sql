import React, { useState } from 'react';
import { Header } from '../components/Header';
import { Hero } from '../components/Hero';
import { QueryInput } from '../components/QueryInput';
import { SQLViewer } from '../components/SQLViewer';
import { Loading } from '../components/Loading';
import { Footer } from '../components/Footer';
import { Toast } from '../components/Toast';
import { predictSql } from '../services/api';

export const Home: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [sqlResult, setSqlResult] = useState<string | null>(null);
  
  const [toast, setToast] = useState({
    isVisible: false,
    message: '',
    type: 'success' as 'success' | 'error'
  });

  const showToast = (message: string, type: 'success' | 'error') => {
    setToast({ isVisible: true, message, type });
  };

  const handleGenerate = async (query: string) => {
    setIsLoading(true);
    setSqlResult(null);
    
    try {
      const response = await predictSql({ question: query });
      
      if (response.sql) {
        setSqlResult(response.sql);
      } else if (response.detail) {
        showToast(response.detail, 'error');
      } else {
        showToast('An unexpected response was received.', 'error');
      }
    } catch (error: any) {
      showToast(error.message || 'Failed to generate SQL', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setSqlResult(null);
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-x-hidden">
      {/* Background ambient gradients */}
      <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-400/10 blur-[100px]" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[50%] h-[50%] rounded-full bg-purple-400/10 blur-[120px]" />
      </div>

      <Header />
      
      <main className="flex-grow flex flex-col items-center justify-center px-4 w-full max-w-[900px] mx-auto z-10 py-12">
        <Hero />
        
        <QueryInput onGenerate={handleGenerate} isLoading={isLoading} />
        
        {isLoading && <Loading />}
        
        {sqlResult && !isLoading && (
          <SQLViewer 
            sql={sqlResult} 
            onClear={handleClear} 
            onCopySuccess={() => showToast('✓ Copied to clipboard', 'success')}
          />
        )}
      </main>
      
      <Footer />
      
      <Toast 
        message={toast.message} 
        type={toast.type} 
        isVisible={toast.isVisible} 
        onClose={() => setToast(prev => ({ ...prev, isVisible: false }))} 
      />
    </div>
  );
};
