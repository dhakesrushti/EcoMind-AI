import React from 'react';
import { MessageSquarePlus, MessageSquare, Database, HardDrive, Leaf } from 'lucide-react';

interface SidebarProps {
  onNewChat: () => void;
  kbStatus: { status: string; document_count: number; chunks_count: number } | null;
}

export const Sidebar: React.FC<SidebarProps> = ({ onNewChat, kbStatus }) => {
  return (
    <div className="w-64 bg-gray-900/50 backdrop-blur-xl border-r border-gray-800 flex flex-col h-full">
      <div className="p-4 border-b border-gray-800 flex items-center gap-3">
        <div className="bg-emerald-500/20 p-2 rounded-lg">
          <Leaf className="w-6 h-6 text-emerald-400" />
        </div>
        <h1 className="text-xl font-semibold text-white tracking-tight">EcoMind AI</h1>
      </div>

      <div className="p-4 flex-1">
        <button
          onClick={onNewChat}
          className="w-full flex items-center gap-2 px-4 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl transition-all shadow-lg shadow-emerald-900/20 mb-6"
        >
          <MessageSquarePlus className="w-5 h-5" />
          <span className="font-medium">New Assessment</span>
        </button>

        <div className="mb-4">
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 px-2">Recent Chats</h2>
          <div className="space-y-1">
            {/* Placeholder for history */}
            <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800/50 rounded-lg transition-colors group">
              <MessageSquare className="w-4 h-4 text-gray-500 group-hover:text-emerald-400" />
              <span className="text-sm truncate">Biodiversity Decline</span>
            </button>
            <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800/50 rounded-lg transition-colors group">
              <MessageSquare className="w-4 h-4 text-gray-500 group-hover:text-emerald-400" />
              <span className="text-sm truncate">Soil Carbon Analysis</span>
            </button>
          </div>
        </div>
      </div>

      <div className="p-4 border-t border-gray-800 space-y-4">
        <div className="flex items-center gap-3 px-2">
          <Database className="w-4 h-4 text-blue-400" />
          <div className="flex flex-col">
            <span className="text-xs text-gray-400">Knowledge Base</span>
            <span className="text-sm font-medium text-gray-200">
              {kbStatus?.status || 'Loading...'}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-3 px-2">
          <HardDrive className="w-4 h-4 text-purple-400" />
          <div className="flex flex-col">
            <span className="text-xs text-gray-400">Documents Indexed</span>
            <span className="text-sm font-medium text-gray-200">
              {kbStatus ? `${kbStatus.document_count} files (${kbStatus.chunks_count} chunks)` : '-'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
