import React, { useState } from 'react';
import { Header } from './components/Header';
import { InputArea } from './components/InputArea';
import { TopicList } from './components/TopicList';
import { ScriptView } from './components/ScriptView';
import { Topic, Script, AppStep } from './types';
import { generateTopics, generateScript } from './services/geminiService';

const App: React.FC = () => {
  const [step, setStep] = useState<AppStep>(AppStep.INPUT);
  const [isLoading, setIsLoading] = useState(false);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<Topic | null>(null);
  const [script, setScript] = useState<Script | null>(null);

  const handleInputSubmit = async (input: string) => {
    setIsLoading(true);
    try {
      const generatedTopics = await generateTopics(input);
      setTopics(generatedTopics);
      setStep(AppStep.TOPICS);
    } catch (error: any) {
      console.error(error);
      alert(`生成选题失败: ${error.message || '未知错误'}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTopicSelect = async (topic: Topic) => {
    setSelectedTopic(topic);
    setIsLoading(true);
    try {
      const generatedScript = await generateScript(topic.title, topic.logic);
      setScript(generatedScript);
      setStep(AppStep.SCRIPT);
    } catch (error: any) {
      console.error(error);
      alert(`生成逐字稿失败: ${error.message || '未知错误'}`);
      setSelectedTopic(null); // Reset selection on error
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    if (step === AppStep.SCRIPT) {
      setStep(AppStep.TOPICS);
      setScript(null);
      setSelectedTopic(null);
    } else if (step === AppStep.TOPICS) {
      setStep(AppStep.INPUT);
      setTopics([]);
    }
  };

  return (
    <div className="min-h-screen bg-[#fafaf9] text-stone-900 selection:bg-stone-200">
      <Header step={step} onBack={handleBack} />
      
      <main className="container mx-auto px-4 py-12">
        {step === AppStep.INPUT && (
          <InputArea onSubmit={handleInputSubmit} isLoading={isLoading} />
        )}

        {step === AppStep.TOPICS && (
          <TopicList 
            topics={topics} 
            onSelect={handleTopicSelect} 
            isLoading={isLoading} 
            selectedTopicId={selectedTopic?.id || null}
          />
        )}

        {step === AppStep.SCRIPT && script && selectedTopic && (
          <ScriptView script={script} topicTitle={selectedTopic.title} />
        )}
      </main>
      
      {/* Footer */}
      <footer className="fixed bottom-0 w-full py-4 text-center text-xs text-stone-400 bg-[#fafaf9]/80 backdrop-blur-sm pointer-events-none z-0">
        <p>Created by Bamboo for Sissy IP · Powered by Google Gemini</p>
      </footer>
    </div>
  );
};

export default App;
