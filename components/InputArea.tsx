import React, { useState } from 'react';
import { SendHorizontal, Loader2 } from 'lucide-react';

interface InputAreaProps {
  onSubmit: (input: string) => void;
  isLoading: boolean;
}

export const InputArea: React.FC<InputAreaProps> = ({ onSubmit, isLoading }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="bg-white p-8 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-stone-100">
        <h2 className="text-2xl font-serif text-stone-800 mb-2">今天想聊什么？</h2>
        <p className="text-stone-500 mb-6 text-sm">
          输入一个关键词、困惑，或者一段素材。Sissy 将为你洞察背后的心理机制。
        </p>
        
        <form onSubmit={handleSubmit} className="relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="例如：为什么我总是这山望着那山高？或者：不敢拒绝别人..."
            className="w-full min-h-[160px] p-4 bg-stone-50 rounded-xl border border-stone-200 text-stone-800 placeholder:text-stone-400 focus:outline-none focus:ring-2 focus:ring-stone-400 focus:border-transparent resize-none transition-all text-lg leading-relaxed"
            disabled={isLoading}
          />
          
          <div className="mt-4 flex justify-end">
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className={`flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 ${
                !input.trim() || isLoading
                  ? 'bg-stone-200 text-stone-400 cursor-not-allowed'
                  : 'bg-stone-800 text-white hover:bg-stone-700 hover:shadow-lg hover:-translate-y-0.5'
              }`}
            >
              {isLoading ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  <span>洞察中...</span>
                </>
              ) : (
                <>
                  <span>生成选题</span>
                  <SendHorizontal size={18} />
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
        {['职场内耗', '情感依赖', '容貌焦虑'].map((tag) => (
          <button
            key={tag}
            onClick={() => setInput(tag)}
            className="p-3 rounded-lg border border-dashed border-stone-300 text-stone-500 text-sm hover:border-stone-500 hover:text-stone-700 transition-colors"
          >
            {tag}
          </button>
        ))}
      </div>
    </div>
  );
};
