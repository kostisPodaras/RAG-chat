import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { DocumentArrowUpIcon, XMarkIcon, CheckIcon } from '@heroicons/react/24/outline';
import { apiService } from '../services/api';

interface DocumentUploadProps {
  onUploadComplete: () => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUploadComplete }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Validate file type
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Only PDF files are allowed');
      return;
    }

    // Validate file size (50MB max)
    if (file.size > 50 * 1024 * 1024) {
      setError('File size must be less than 50MB');
      return;
    }

    setUploading(true);
    setError(null);
    setUploadResult(null);

    try {
      const result = await apiService.uploadDocument(file);
      setUploadResult(`✅ ${result.message}`);
      onUploadComplete();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  }, [onUploadComplete]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    disabled: uploading
  });

  const clearMessages = () => {
    setError(null);
    setUploadResult(null);
  };

  return (
    <div className="bg-white rounded-lg border border-rag-border p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <DocumentArrowUpIcon className="w-5 h-5 text-rag-primary" />
        Upload Documents
      </h3>
      
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-rag-primary bg-rag-primary/5' : 'border-rag-border hover:border-rag-primary/50'}
          ${uploading ? 'pointer-events-none opacity-50' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <DocumentArrowUpIcon className="w-12 h-12 text-rag-secondary mx-auto mb-4" />
        
        {uploading ? (
          <div className="space-y-2">
            <div className="flex items-center justify-center gap-2">
              <div className="w-5 h-5 border-2 border-rag-primary border-t-transparent rounded-full animate-spin" />
              <span className="text-rag-primary font-medium">Uploading...</span>
            </div>
            <p className="text-sm text-rag-secondary">
              Processing your document and creating embeddings...
            </p>
          </div>
        ) : isDragActive ? (
          <p className="text-rag-primary font-medium">Drop the PDF file here!</p>
        ) : (
          <div className="space-y-2">
            <p className="text-gray-900 font-medium">
              Drop a PDF file here, or click to select
            </p>
            <p className="text-sm text-rag-secondary">
              Maximum file size: 50MB
            </p>
          </div>
        )}
      </div>

      {/* Messages */}
      {(error || uploadResult) && (
        <div className="mt-4">
          {error && (
            <div className="flex items-start gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800">
              <XMarkIcon className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm">{error}</p>
              </div>
              <button
                onClick={clearMessages}
                className="text-red-500 hover:text-red-700"
              >
                <XMarkIcon className="w-4 h-4" />
              </button>
            </div>
          )}
          
          {uploadResult && (
            <div className="flex items-start gap-2 p-3 bg-green-50 border border-green-200 rounded-lg text-green-800">
              <CheckIcon className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm">{uploadResult}</p>
              </div>
              <button
                onClick={clearMessages}
                className="text-green-500 hover:text-green-700"
              >
                <XMarkIcon className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      )}

      <div className="mt-4 text-xs text-rag-secondary">
        💡 Tip: Upload PDFs to enable AI to answer questions about your documents
      </div>
    </div>
  );
};