import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import { apiService } from '../services/api';
import { ChatMessage } from '../components/ChatMessage';
import { ChatInput } from '../components/ChatInput';
import { DocumentUpload } from '../components/DocumentUpload';
import { DocumentList } from '../components/DocumentList';
import { DocumentTextIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';

interface ChatPageProps {
  sessionId: number | null;
  onSessionCreated: (sessionId: number) => void;
}

export const ChatPage: React.FC<ChatPageProps> = ({ sessionId, onSessionCreated }) => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [showDocuments, setShowDocuments] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (sessionId) {
      loadMessages();
    } else {
      setMessages([]);
    }
  }, [sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadMessages = async () => {
    if (!sessionId) return;
    
    setLoading(true);
    try {
      const data = await apiService.getChatMessages(sessionId);
      setMessages(data);
    } catch (error) {
      console.error('Error loading messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    setSending(true);
    
    try {
      let currentSessionId = sessionId;
      
      // Create new session if needed
      if (!currentSessionId) {
        const newSession = await apiService.createChatSession(
          content.length > 50 ? content.substring(0, 50) + '...' : content
        );
        currentSessionId = newSession.id;
        onSessionCreated(currentSessionId);
      }

      // Send message
      await apiService.sendMessage(currentSessionId, content);
      
      // Refresh messages
      await loadMessages();
      
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message. Please try again.');
    } finally {
      setSending(false);
    }
  };

  const handleDocumentChange = () => {
    // Refresh document list when documents change
    if ((window as any).refreshDocuments) {
      (window as any).refreshDocuments();
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full">
      {/* Header */}
      <div className="border-b border-rag-border bg-white px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold text-gray-900">
            {sessionId ? 'Chat Session' : 'New Conversation'}
          </h1>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowDocuments(!showDocuments)}
              className={`
                flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors
                ${showDocuments 
                  ? 'bg-rag-primary text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }
              `}
            >
              <DocumentTextIcon className="w-4 h-4" />
              {showDocuments ? 'Hide' : 'Show'} Documents
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto">
            {loading ? (
              <div className="flex items-center justify-center h-full">
                <div className="flex items-center gap-2 text-rag-secondary">
                  <div className="w-5 h-5 border-2 border-rag-primary border-t-transparent rounded-full animate-spin" />
                  Loading messages...
                </div>
              </div>
            ) : messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center max-w-md">
                  <Cog6ToothIcon className="w-16 h-16 text-rag-secondary mx-auto mb-4 opacity-50" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Welcome to RAG Chat
                  </h3>
                  <p className="text-rag-secondary mb-4">
                    Upload PDF documents and ask questions about them. 
                    All processing happens locally for maximum privacy.
                  </p>
                  <div className="text-sm text-rag-secondary bg-rag-bg rounded-lg p-3">
                    💡 Start by uploading a document or asking a general question
                  </div>
                </div>
              </div>
            ) : (
              <div>
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Chat Input */}
          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={sending}
            placeholder={
              messages.length === 0 
                ? "Ask a question or upload a document to get started..."
                : "Ask a follow-up question..."
            }
          />
        </div>

        {/* Document Panel */}
        {showDocuments && (
          <div className="w-96 border-l border-rag-border bg-rag-bg p-6 overflow-y-auto">
            <div className="space-y-6">
              <DocumentUpload onUploadComplete={handleDocumentChange} />
              <DocumentList 
                onDocumentChange={handleDocumentChange} 
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};