import React, { useState } from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import { UserIcon, CpuChipIcon, DocumentIcon, EyeIcon } from '@heroicons/react/24/outline';
import { formatDistanceToNow } from 'date-fns';
import { PDFModal } from './PDFModal';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const [selectedPDF, setSelectedPDF] = useState<{ filename: string; page?: number } | null>(null);
  
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
                  className="bg-white border border-rag-border rounded-lg p-3 text-xs hover:border-rag-primary/50 transition-colors group"
                >
                  <div className="flex items-center justify-between mb-1">
                    <button
                      onClick={() => setSelectedPDF({ filename: source.filename, page: source.page })}
                      className="font-medium text-rag-primary hover:text-rag-primary/80 transition-colors flex items-center gap-1.5"
                    >
                      <DocumentIcon className="w-3 h-3" />
                      {source.filename}
                      <EyeIcon className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                    <span className="text-rag-secondary">
                      Page {source.page}
                    </span>
                  </div>
                  <p className="text-rag-secondary leading-relaxed">
                    {source.content}
                  </p>
                  <div className="mt-2 pt-2 border-t border-rag-border/50">
                    <button
                      onClick={() => setSelectedPDF({ filename: source.filename, page: source.page })}
                      className="text-xs text-rag-primary hover:text-rag-primary/80 transition-colors font-medium"
                    >
                      Click to view document →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      
      {/* PDF Modal */}
      {selectedPDF && (
        <PDFModal
          isOpen={true}
          onClose={() => setSelectedPDF(null)}
          filename={selectedPDF.filename}
          page={selectedPDF.page}
        />
      )}
    </div>
  );
};