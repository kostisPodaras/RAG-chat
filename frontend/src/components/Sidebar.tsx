import React, { useState, useEffect } from 'react';
import { ChatSession } from '../types';
import { apiService } from '../services/api';
import { PlusIcon, TrashIcon, ChatBubbleLeftIcon } from '@heroicons/react/24/outline';
import { formatDistanceToNow } from 'date-fns';

interface SidebarProps {
  currentSessionId: number | null;
  onSessionSelect: (sessionId: number) => void;
  onNewSession: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  currentSessionId, 
  onSessionSelect, 
  onNewSession
}) => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const data = await apiService.getChatSessions();
      setSessions(data);
    } catch (error) {
      console.error('Error loading sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSession = async (sessionId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm('Delete this chat session?')) return;

    try {
      await apiService.deleteChatSession(sessionId);
      setSessions(sessions.filter(s => s.id !== sessionId));
      if (currentSessionId === sessionId) {
        onNewSession();
      }
    } catch (error) {
      console.error('Error deleting session:', error);
      alert('Failed to delete session');
    }
  };

  const refreshSessions = () => {
    loadSessions();
  };

  // Expose refresh function globally for now
  React.useEffect(() => {
    (window as any).refreshSidebar = refreshSessions;
  }, []);

  return (
    <div className="w-64 bg-rag-sidebar border-r border-rag-border h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-rag-border">
        <button
          onClick={onNewSession}
          className="w-full flex items-center gap-2 px-3 py-2 bg-rag-primary text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          <PlusIcon className="w-4 h-4" />
          New Chat
        </button>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-4 text-rag-secondary">Loading...</div>
        ) : sessions.length === 0 ? (
          <div className="p-4 text-rag-secondary text-sm">
            No chat sessions yet. Start a new conversation!
          </div>
        ) : (
          <div className="p-2">
            {sessions.map((session) => (
              <div
                key={session.id}
                onClick={() => onSessionSelect(session.id)}
                className={`
                  group flex items-center justify-between p-3 rounded-lg cursor-pointer mb-1
                  ${currentSessionId === session.id 
                    ? 'bg-rag-primary/10 border border-rag-primary/20' 
                    : 'hover:bg-gray-100'
                  }
                `}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-start gap-2">
                    <ChatBubbleLeftIcon className="w-4 h-4 text-rag-secondary mt-0.5 flex-shrink-0" />
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {session.title}
                      </p>
                      <p className="text-xs text-rag-secondary">
                        {formatDistanceToNow(new Date(session.updated_at), { addSuffix: true })}
                      </p>
                    </div>
                  </div>
                </div>
                <button
                  onClick={(e) => handleDeleteSession(session.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-100 rounded transition-all"
                  title="Delete session"
                >
                  <TrashIcon className="w-4 h-4 text-red-500" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-rag-border">
        <div className="text-xs text-rag-secondary">
          🔒 All data stays local & private
        </div>
      </div>
    </div>
  );
};