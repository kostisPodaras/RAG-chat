import React, { useState, useEffect } from 'react';
import { Document } from '../types';
import { apiService } from '../services/api';
import { DocumentIcon, TrashIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { formatDistanceToNow } from 'date-fns';

interface DocumentListProps {
  onDocumentChange: () => void;
}

export const DocumentList: React.FC<DocumentListProps> = ({ onDocumentChange }) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState<string | null>(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const data = await apiService.getDocuments();
      setDocuments(data);
    } catch (error) {
      console.error('Error loading documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteDocument = async (filename: string) => {
    if (!window.confirm(`Delete "${filename}"? This will remove it from the vector database.`)) {
      return;
    }

    setDeleting(filename);
    try {
      await apiService.deleteDocument(filename);
      setDocuments(documents.filter(doc => doc.filename !== filename));
      onDocumentChange();
    } catch (error) {
      console.error('Error deleting document:', error);
      alert('Failed to delete document');
    } finally {
      setDeleting(null);
    }
  };

  // Expose refresh function globally for now
  React.useEffect(() => {
    (window as any).refreshDocuments = loadDocuments;
  }, []);

  if (loading) {
    return (
      <div className="bg-white rounded-lg border border-rag-border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Document Library</h3>
        <div className="text-rag-secondary">Loading...</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-rag-border p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <DocumentIcon className="w-5 h-5 text-rag-primary" />
        Document Library ({documents.length})
      </h3>
      
      {documents.length === 0 ? (
        <div className="text-center py-8">
          <DocumentIcon className="w-12 h-12 text-rag-secondary mx-auto mb-4 opacity-50" />
          <p className="text-rag-secondary">No documents uploaded yet</p>
          <p className="text-sm text-rag-secondary mt-1">
            Upload a PDF to start asking questions about it
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {documents.map((doc) => (
            <div
              key={doc.filename}
              className="flex items-center justify-between p-3 border border-rag-border rounded-lg hover:bg-rag-bg transition-colors"
            >
              <div className="flex items-start gap-3 flex-1 min-w-0">
                <DocumentIcon className="w-5 h-5 text-rag-primary flex-shrink-0 mt-0.5" />
                <div className="min-w-0 flex-1">
                  <p className="font-medium text-gray-900 truncate" title={doc.filename}>
                    {doc.filename}
                  </p>
                  <div className="flex items-center gap-4 mt-1 text-xs text-rag-secondary">
                    <span className="flex items-center gap-1">
                      <CalendarIcon className="w-3 h-3" />
                      {formatDistanceToNow(new Date(doc.upload_date), { addSuffix: true })}
                    </span>
                    <span>{doc.pages} pages</span>
                    <span>{doc.size_mb.toFixed(1)} MB</span>
                  </div>
                </div>
              </div>
              
              <button
                onClick={() => handleDeleteDocument(doc.filename)}
                disabled={deleting === doc.filename}
                className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                title="Delete document"
              >
                {deleting === doc.filename ? (
                  <div className="w-4 h-4 border-2 border-red-500 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <TrashIcon className="w-4 h-4" />
                )}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};