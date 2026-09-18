import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Leaf, Loader2 } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface ChatPanelProps {
  messages: Message[];
  isLoading: boolean;
  onSendMessage: (msg: string) => void;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ messages, isLoading, onSendMessage }) => {
  const [input, setInput] = useState('');
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-[#0a0a0a] relative">
      <div className="flex-1 overflow-y-auto p-4 space-y-6 pb-32">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center px-4">
            <div className="w-16 h-16 bg-emerald-500/10 rounded-2xl flex items-center justify-center mb-6">
              <Leaf className="w-8 h-8 text-emerald-500" />
            </div>
            <h2 className="text-2xl font-semibold text-white mb-2">Welcome to EcoMind AI</h2>
            <p className="text-gray-400 max-w-md">
              Your AI Environmental Consultant. Describe your environmental situation or ask for recommendations based on scientifically grounded evidence.
            </p>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-4 max-w-4xl mx-auto ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-emerald-900/50">
                  <Leaf className="w-4 h-4 text-white" />
                </div>
              )}
              <div
                className={`px-5 py-4 rounded-2xl max-w-[85%] ${
                  msg.role === 'user'
                    ? 'bg-emerald-600 text-white rounded-br-none shadow-lg shadow-emerald-900/20'
                    : 'bg-gray-800/50 text-gray-200 border border-gray-700/50 rounded-bl-none'
                }`}
              >
                <div className="whitespace-pre-wrap leading-relaxed text-[15px]">{msg.content}</div>
              </div>
              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center shrink-0 mt-1">
                  <User className="w-4 h-4 text-gray-300" />
                </div>
              )}
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex gap-4 max-w-4xl mx-auto justify-start">
            <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center shrink-0 mt-1">
              <Leaf className="w-4 h-4 text-white" />
            </div>
            <div className="px-5 py-4 rounded-2xl bg-gray-800/50 border border-gray-700/50 rounded-bl-none flex items-center gap-3 text-gray-400">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm">Analyzing environmental variables...</span>
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>

      <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-[#0a0a0a] via-[#0a0a0a] to-transparent pt-12">
        <form
          onSubmit={handleSubmit}
          className="max-w-4xl mx-auto relative flex items-center"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your environmental query..."
            className="w-full bg-gray-900 border border-gray-700/50 rounded-xl pl-5 pr-12 py-4 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all shadow-xl"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 p-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-800 disabled:text-gray-500 text-white rounded-lg transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
        <div className="text-center mt-2">
          <span className="text-[11px] text-gray-600">EcoMind AI can make mistakes. Consider verifying important environmental decisions.</span>
        </div>
      </div>
    </div>
  );
};
