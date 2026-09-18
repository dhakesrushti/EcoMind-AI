import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatPanel } from './components/ChatPanel';
import { RightPanel } from './components/RightPanel';
import { chat, getKbStatus, ChatResponse, StatusResponse } from './services/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string>(Math.random().toString(36).substring(7));
  const [isLoading, setIsLoading] = useState(false);
  const [kbStatus, setKbStatus] = useState<StatusResponse | null>(null);
  const [lastResponse, setLastResponse] = useState<ChatResponse | null>(null);

  useEffect(() => {
    const fetchKbStatus = async () => {
      try {
        const status = await getKbStatus();
        setKbStatus(status);
      } catch (error) {
        console.error('Failed to fetch KB status:', error);
        setKbStatus({ status: 'Error', document_count: 0, chunks_count: 0 });
      }
    };
    fetchKbStatus();
  }, []);

  const handleNewChat = () => {
    setMessages([]);
    setSessionId(Math.random().toString(36).substring(7));
    setLastResponse(null);
  };

  const handleSendMessage = async (text: string) => {
    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: text };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await chat({ session_id: sessionId, message: text });
      setLastResponse(response);
      
      let assistantContent = '';
      if (response.needs_more_info) {
        assistantContent = response.analysis;
      } else {
        assistantContent = `**ANALYSIS**\n${response.analysis}\n\n`;
        if (response.recommendations.length > 0) {
            assistantContent += `**RECOMMENDATIONS**\n${response.recommendations.map(r => `• ${r}`).join('\n')}\n\n`;
        }
        if (response.expected_impact.length > 0) {
            assistantContent += `**EXPECTED IMPACT**\n${response.expected_impact.map(e => `• ${e}`).join('\n')}\n\n`;
        }
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: assistantContent.trim()
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error communicating with the environmental reasoning engine.'
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#050505] text-gray-200 overflow-hidden font-sans">
      <Sidebar onNewChat={handleNewChat} kbStatus={kbStatus} />
      <ChatPanel messages={messages} isLoading={isLoading} onSendMessage={handleSendMessage} />
      <RightPanel lastResponse={lastResponse} />
    </div>
  );
}

export default App;
