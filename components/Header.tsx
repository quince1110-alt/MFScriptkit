import React from 'react';
import { Sparkles, ArrowLeft } from 'lucide-react';
import { AppStep } from '../types';

interface HeaderProps {
  step: AppStep;
  onBack: () => void;
}

export const Header: React.FC<HeaderProps> = ({ step, onBack }) => {
  return (
    <header className="py-6 px-4 md:px-8 border-b border-stone-200 bg-white/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-3xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          {step !== AppStep.INPUT && (
             <button 
             onClick={onBack}
             className="p-2 -ml-2 hover:bg-stone-100 rounded-full transition-colors text-stone-600"
           >
             <ArrowLeft size={20} />
           </button>
          )}
          <div className="flex items-center gap-2">
            <div className="bg-stone-800 text-white p-1.5 rounded-lg">
              <Sparkles size={18} />
            </div>
            <div>
              <h1 className="text-xl font-serif font-bold text-stone-900 tracking-tight leading-none">
                Sissy IP
              </h1>
              <p className="text-xs text-stone-500 font-medium tracking-wide">
                MINDFULNESS CONTENT
              </p>
            </div>
          </div>
        </div>
        <div className="hidden md:block">
            <span className="text-xs font-medium px-3 py-1 bg-sage-100 text-sage-800 rounded-full border border-sage-200">
                正念 · 觉醒 · 肉身解题
            </span>
        </div>
      </div>
    </header>
  );
};
