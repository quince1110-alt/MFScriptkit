import React from 'react';
import { Topic } from '../types';
import { ChevronRight, Loader2, Sparkles } from 'lucide-react';

interface TopicListProps {
  topics: Topic[];
  onSelect: (topic: Topic) => void;
  isLoading: boolean;
  selectedTopicId: string | null;
}

export const TopicList: React.FC<TopicListProps> = ({ topics, onSelect, isLoading, selectedTopicId }) => {
  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="text-center mb-10 animate-in fade-in duration-700">
        <h2 className="text-3xl font-serif text-stone-800 mb-3">洞察已完成</h2>
        <p className="text-stone-600">请选择一个最能击中“痛点”的切入角度</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {topics.map((topic, index) => (
          <div
            key={topic.id}
            onClick={() => !isLoading && onSelect(topic)}
            className={`group relative p-6 rounded-2xl border transition-all duration-300 cursor-pointer flex flex-col h-full animate-in fade-in slide-in-from-bottom-8 fill-mode-backwards
              ${selectedTopicId === topic.id 
                ? 'bg-stone-800 border-stone-800 ring-4 ring-stone-200' 
                : 'bg-white border-stone-200 hover:border-stone-400 hover:shadow-xl hover:-translate-y-1'
              }
              ${isLoading && selectedTopicId !== topic.id ? 'opacity-50 pointer-events-none' : ''}
            `}
            style={{ animationDelay: `${index * 150}ms` }}
          >
             {/* Decorative Number */}
            <div className={`absolute -top-4 -left-2 text-6xl font-serif opacity-10 font-bold select-none ${selectedTopicId === topic.id ? 'text-white' : 'text-stone-900'}`}>
                0{index + 1}
            </div>

            <div className="relative z-10 flex flex-col h-full">
              <h3 className={`text-xl font-bold mb-4 leading-snug font-serif ${selectedTopicId === topic.id ? 'text-white' : 'text-stone-900'}`}>
                {topic.title}
              </h3>
              
              <div className={`flex-grow text-sm mb-6 leading-relaxed ${selectedTopicId === topic.id ? 'text-stone-300' : 'text-stone-600'}`}>
                <span className={`block text-xs uppercase tracking-wider font-bold mb-2 ${selectedTopicId === topic.id ? 'text-stone-400' : 'text-stone-400'}`}>
                    底层逻辑
                </span>
                {topic.logic}
              </div>

              <div className={`mt-auto pt-4 border-t flex items-center justify-between ${selectedTopicId === topic.id ? 'border-stone-700 text-stone-200' : 'border-stone-100 text-stone-900'}`}>
                <span className="text-xs font-medium tracking-widest uppercase">生成逐字稿</span>
                {isLoading && selectedTopicId === topic.id ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : (
                  <div className={`p-1 rounded-full transition-transform group-hover:translate-x-1 ${selectedTopicId === topic.id ? 'bg-stone-700' : 'bg-stone-100'}`}>
                     <ChevronRight size={16} />
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
