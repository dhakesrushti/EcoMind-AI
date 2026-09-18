import React from 'react';
import { Settings, FileText, BrainCircuit, Activity, BookOpen } from 'lucide-react';
import { ChatResponse } from '../services/api';

interface RightPanelProps {
  lastResponse: ChatResponse | null;
}

export const RightPanel: React.FC<RightPanelProps> = ({ lastResponse }) => {
  return (
    <div className="w-80 bg-gray-900/50 backdrop-blur-xl border-l border-gray-800 flex flex-col h-full overflow-y-auto">
      <div className="p-4 border-b border-gray-800">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <Activity className="w-5 h-5 text-emerald-400" />
          Intelligence Hub
        </h2>
      </div>

      <div className="p-4 space-y-6">
        {/* Environmental Variables */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <Settings className="w-4 h-4" />
            Current Variables
          </h3>
          <div className="bg-gray-800/40 rounded-xl p-3 border border-gray-700/50">
            {lastResponse?.state && Object.keys(lastResponse.state).length > 0 ? (
              <div className="space-y-2">
                {Object.entries(lastResponse.state).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center text-sm">
                    <span className="text-gray-400 capitalize">{key.replace('_', ' ')}</span>
                    <span className="font-medium text-emerald-400">{String(value)}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-500 italic text-center py-2">No variables detected yet.</p>
            )}
          </div>
        </div>

        {/* Reasoning Trace */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <BrainCircuit className="w-4 h-4" />
            Reasoning Trace
          </h3>
          <div className="bg-gray-800/40 rounded-xl p-3 border border-gray-700/50">
            {lastResponse?.reasoning_trace ? (
              <pre className="text-xs text-blue-300 font-mono whitespace-pre-wrap">
                {lastResponse.reasoning_trace}
              </pre>
            ) : (
              <p className="text-sm text-gray-500 italic text-center py-2">Awaiting reasoning execution.</p>
            )}
          </div>
        </div>

        {/* Scientific Evidence */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Scientific Evidence
          </h3>
          <div className="space-y-2">
            {lastResponse?.scientific_evidence && lastResponse.scientific_evidence.length > 0 ? (
              lastResponse.scientific_evidence.map((evidence, idx) => (
                <div key={idx} className="bg-emerald-900/10 border border-emerald-500/20 rounded-xl p-3">
                  <p className="text-xs text-emerald-200/80 leading-relaxed italic">"{evidence}"</p>
                </div>
              ))
            ) : (
              <div className="bg-gray-800/40 rounded-xl p-3 border border-gray-700/50">
                <p className="text-sm text-gray-500 italic text-center py-2">No evidence retrieved.</p>
              </div>
            )}
          </div>
        </div>

        {/* Sources */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            Retrieved Sources
          </h3>
          <div className="space-y-2">
            {lastResponse?.sources && lastResponse.sources.length > 0 ? (
              lastResponse.sources.map((source, idx) => (
                <div key={idx} className="flex items-center gap-2 text-xs text-gray-300 bg-gray-800/60 p-2 rounded-lg border border-gray-700/50">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                  {source}
                </div>
              ))
            ) : (
              <div className="bg-gray-800/40 rounded-xl p-3 border border-gray-700/50">
                <p className="text-sm text-gray-500 italic text-center py-2">No sources mapped.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
