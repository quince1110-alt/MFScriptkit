import React, { useState, useEffect, useRef } from 'react';
import { Script } from '../types';
import { Copy, Check, Brain, RefreshCcw, Zap, Heart, MessageCircle, MonitorPlay, X, Type, Play, Pause, FlipHorizontal, Minus, Plus } from 'lucide-react';

interface ScriptViewProps {
  script: Script;
  topicTitle: string;
}

export const ScriptView: React.FC<ScriptViewProps> = ({ script, topicTitle }) => {
  const [copied, setCopied] = useState(false);
  
  // Teleprompter State
  const [isTeleprompterOpen, setIsTeleprompterOpen] = useState(false);
  const [fontSize, setFontSize] = useState(48); // px
  const [scrollSpeed, setScrollSpeed] = useState(0); // 0 = paused
  const [isMirrored, setIsMirrored] = useState(false);
  const scrollerRef = useRef<HTMLDivElement>(null);

  const handleCopy = () => {
    const text = `
标题：${topicTitle}

[黄金开头]
${script.hook}

[深度归因]
${script.attribution}

[认知翻转]
${script.reversal}

[正念解题]
${script.solution}

[结尾引流]
${script.cta}
    `.trim();
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Auto-scroll logic
  useEffect(() => {
    let animationFrameId: number;
    
    const scroll = () => {
      if (scrollerRef.current && scrollSpeed > 0) {
        // Adjust speed multiplier as needed for smooth scrolling
        scrollerRef.current.scrollTop += scrollSpeed * 0.5;
        animationFrameId = requestAnimationFrame(scroll);
      }
    };

    if (isTeleprompterOpen && scrollSpeed > 0) {
      animationFrameId = requestAnimationFrame(scroll);
    }

    return () => cancelAnimationFrame(animationFrameId);
  }, [isTeleprompterOpen, scrollSpeed]);

  const sections = [
    {
      title: "黄金开头 (The Hook)",
      icon: Zap,
      time: "0-5s",
      content: script.hook,
      color: "text-amber-600",
      bg: "bg-amber-50 border-amber-100"
    },
    {
      title: "深度归因 (Deep Attribution)",
      icon: Brain,
      time: "5-25s",
      content: script.attribution,
      color: "text-blue-600",
      bg: "bg-blue-50 border-blue-100"
    },
    {
      title: "认知翻转 (Cognitive Reversal)",
      icon: RefreshCcw,
      time: "25-40s",
      content: script.reversal,
      color: "text-purple-600",
      bg: "bg-purple-50 border-purple-100"
    },
    {
      title: "正念解题 (Mindfulness Solution)",
      icon: Heart,
      time: "40-55s",
      content: script.solution,
      color: "text-emerald-600",
      bg: "bg-emerald-50 border-emerald-100"
    },
    {
      title: "结尾与引流 (CTA)",
      icon: MessageCircle,
      time: "55-60s",
      content: script.cta,
      color: "text-rose-600",
      bg: "bg-rose-50 border-rose-100"
    }
  ];

  const fullScriptContent = sections.map(s => s.content).join('\n\n');

  return (
    <>
      <div className="w-full max-w-3xl mx-auto pb-20 animate-in fade-in slide-in-from-bottom-8 duration-700">
        
        <div className="flex items-end justify-between mb-8">
          <div>
             <h2 className="text-sm text-stone-500 font-medium mb-1 uppercase tracking-wider">当前选题</h2> 
             <h1 className="text-3xl font-serif font-bold text-stone-900">{topicTitle}</h1>
          </div>
          <div className="flex gap-2">
            <button 
              onClick={() => setIsTeleprompterOpen(true)}
              className="flex items-center gap-2 px-4 py-2 bg-white text-stone-700 border border-stone-200 rounded-lg hover:bg-stone-50 hover:border-stone-300 transition-colors shadow-sm text-sm font-medium"
            >
              <MonitorPlay size={16} />
              <span className="hidden sm:inline">提词模式</span>
            </button>
            <button 
              onClick={handleCopy}
              className="flex items-center gap-2 px-4 py-2 bg-stone-900 text-white rounded-lg hover:bg-stone-700 transition-colors shadow-sm text-sm font-medium"
            >
              {copied ? <Check size={16} /> : <Copy size={16} />}
              {copied ? '已复制' : '复制全文'}
            </button>
          </div>
        </div>

        <div className="space-y-6 relative before:absolute before:left-[27px] before:top-8 before:bottom-8 before:w-0.5 before:bg-stone-200 before:content-['']">
          {sections.map((section, idx) => {
            const Icon = section.icon;
            return (
              <div key={idx} className="relative pl-16 group">
                {/* Timeline Dot */}
                <div className={`absolute left-0 top-0 w-14 h-14 flex flex-col items-center justify-center bg-white border-2 rounded-xl z-10 transition-colors duration-300 ${section.bg.replace('bg-', 'border-').replace('50', '200')}`}>
                   <Icon size={20} className={`mb-1 ${section.color}`} />
                   <span className="text-[10px] font-bold text-stone-400 font-mono">{section.time}</span>
                </div>

                {/* Card */}
                <div className={`p-6 rounded-2xl border ${section.bg} transition-all duration-300 hover:shadow-md`}>
                  <h3 className={`font-serif font-bold text-lg mb-3 flex items-center gap-2 ${section.color}`}>
                    {section.title}
                  </h3>
                  <p className="text-stone-800 leading-relaxed whitespace-pre-line text-lg">
                    {section.content}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Teleprompter Overlay */}
      {isTeleprompterOpen && (
        <div className="fixed inset-0 z-[100] bg-black text-white flex flex-col animate-in fade-in duration-300">
          {/* Toolbar */}
          <div className="flex flex-wrap items-center justify-between p-4 bg-stone-900/90 border-b border-stone-800 backdrop-blur-md shrink-0 gap-4">
            
            <button 
              onClick={() => setIsTeleprompterOpen(false)}
              className="p-2 hover:bg-stone-800 rounded-full transition-colors text-stone-400 hover:text-white"
            >
              <X size={24} />
            </button>

            <div className="flex items-center gap-6 flex-1 justify-center min-w-[200px]">
              {/* Font Size Control */}
              <div className="flex items-center gap-2 bg-stone-800 rounded-lg p-1">
                <button 
                  onClick={() => setFontSize(Math.max(24, fontSize - 4))}
                  className="p-2 hover:bg-stone-700 rounded-md text-stone-400 hover:text-white"
                >
                  <Minus size={16} />
                </button>
                <div className="flex items-center gap-1 w-16 justify-center">
                  <Type size={16} className="text-stone-400" />
                  <span className="text-sm font-mono">{fontSize}</span>
                </div>
                <button 
                  onClick={() => setFontSize(Math.min(120, fontSize + 4))}
                  className="p-2 hover:bg-stone-700 rounded-md text-stone-400 hover:text-white"
                >
                  <Plus size={16} />
                </button>
              </div>

              {/* Scroll Speed Control */}
              <div className="flex items-center gap-3 bg-stone-800 rounded-lg p-2 px-4">
                <button 
                   onClick={() => setScrollSpeed(scrollSpeed === 0 ? 1 : 0)}
                   className={`${scrollSpeed > 0 ? 'text-green-400' : 'text-stone-400'}`}
                >
                  {scrollSpeed > 0 ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" />}
                </button>
                <input 
                  type="range" 
                  min="0" 
                  max="10" 
                  step="0.5"
                  value={scrollSpeed}
                  onChange={(e) => setScrollSpeed(parseFloat(e.target.value))}
                  className="w-24 accent-stone-200 h-1 bg-stone-600 rounded-lg appearance-none cursor-pointer"
                />
                <span className="text-xs font-mono text-stone-400 w-8 text-right">{scrollSpeed > 0 ? `${scrollSpeed}x` : 'OFF'}</span>
              </div>

               {/* Mirror Control */}
               <button 
                  onClick={() => setIsMirrored(!isMirrored)}
                  className={`p-2 rounded-lg transition-colors ${isMirrored ? 'bg-stone-700 text-blue-300' : 'hover:bg-stone-800 text-stone-400'}`}
                  title="镜像模式"
                >
                  <FlipHorizontal size={20} />
                </button>
            </div>
            
            <div className="w-10"></div> {/* Spacer for balance */}
          </div>

          {/* Text Area */}
          <div 
            ref={scrollerRef}
            className="flex-1 overflow-y-auto px-4 md:px-20 scroll-smooth no-scrollbar"
            onClick={() => setScrollSpeed(scrollSpeed > 0 ? 0 : 1)} // Click to toggle play/pause
          >
            <div 
              className={`max-w-5xl mx-auto py-20 pb-[60vh] transition-transform duration-300 origin-center ${isMirrored ? 'scale-x-[-1]' : ''}`}
            >
              <h1 className="text-stone-500 font-serif mb-12 text-center" style={{ fontSize: fontSize * 0.6 }}>
                {topicTitle}
              </h1>
              <div 
                className="font-sans font-medium leading-relaxed tracking-wide text-center whitespace-pre-wrap outline-none"
                style={{ fontSize: `${fontSize}px` }}
              >
                {fullScriptContent}
              </div>
            </div>
          </div>
          
          {/* Scroll Overlay Indicator */}
          <div className="absolute left-0 right-0 top-[80px] h-20 bg-gradient-to-b from-black to-transparent pointer-events-none"></div>
          <div className="absolute left-0 right-0 bottom-0 h-20 bg-gradient-to-t from-black to-transparent pointer-events-none"></div>
          
          {/* Reading Guide Line (Optional, centralized line) */}
          <div className="absolute top-1/2 left-4 right-4 h-[2px] bg-red-500/20 pointer-events-none transform -translate-y-1/2 rounded-full"></div>
        </div>
      )}
    </>
  );
};
