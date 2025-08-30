import React from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import { UserIcon, CpuChipIcon, DocumentIcon } from '@heroicons/react/24/outline';
import { formatDistanceToNow } from 'date-fns';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex gap-3 p-4 ${isUser ? 'bg-transparent' : 'bg-rag-bg'}`}>
      {/* Avatar */}
      <div className={`
        w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0
        ${isUser ? 'bg-rag-primary text-white' : 'bg-rag-accent text-white'}
      `}>
        {isUser ? (
          <UserIcon className="w-5 h-5" />
        ) : (
          <CpuChipIcon className="w-5 h-5" />
        )}
      </div>
      
      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className="font-medium text-sm text-gray-900">
            {isUser ? 'You' : 'AI Assistant'}
          </span>
          <span className="text-xs text-rag-secondary">
            {formatDistanceToNow(new Date(message.created_at), { addSuffix: true })}
          </span>
        </div>
        
        <div className="prose prose-sm max-w-none">
          <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
            {message.content}
          </p>
        </div>
        
        {/* Sources */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3 border-t border-rag-border pt-3">
            <div className="text-xs font-medium text-rag-secondary mb-2 flex items-center gap-1">
              <DocumentIcon className="w-3 h-3" />
              Sources:
            </div>
            <div className="space-y-2">
              {message.sources.map((source, index) => (
                <div 
                  key={index}
                  className="bg-white border border-rag-border rounded-lg p-3 text-xs"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-rag-primary">
                      {source.filename}
                    </span>
                    <span className="text-rag-secondary">
                      Page {source.page}
                    </span>
                  </div>
                  <p className="text-rag-secondary leading-relaxed">
                    {source.content}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};