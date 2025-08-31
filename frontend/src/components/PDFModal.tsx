import React, { useState } from 'react';
import { Dialog } from '@headlessui/react';
import { XMarkIcon, ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline';

interface PDFModalProps {
  isOpen: boolean;
  onClose: () => void;
  filename: string;
  page?: number;
}

export const PDFModal: React.FC<PDFModalProps> = ({
  isOpen,
  onClose,
  filename,
  page
}) => {
  const [showFallback, setShowFallback] = useState(false);
  const pdfUrl = `http://localhost:8001/api/v1/documents/view/${encodeURIComponent(filename)}${page ? `#page=${page}` : ''}`;
  return (
    <Dialog
      open={isOpen}
      onClose={onClose}
      className="relative z-50"
    >
      {/* Background overlay */}
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
      
      {/* Full-screen modal */}
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <Dialog.Panel className="mx-auto max-w-7xl w-full h-full bg-white rounded-lg shadow-xl flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <div className="flex items-center gap-3">
              <Dialog.Title className="text-lg font-semibold text-gray-900">
                {filename}
              </Dialog.Title>
              {page && (
                <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                  Page {page}
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => window.open(pdfUrl, '_blank')}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                title="Open in new tab"
              >
                <ArrowTopRightOnSquareIcon className="w-5 h-5 text-gray-500" />
              </button>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <XMarkIcon className="w-5 h-5 text-gray-500" />
              </button>
            </div>
          </div>
          
          {/* PDF Content */}
          <div className="flex-1 overflow-hidden bg-gray-100">
            {!showFallback ? (
              <iframe
                src={pdfUrl}
                className="w-full h-full border-0"
                title={`PDF Viewer - ${filename}`}
                onError={(e) => {
                  console.error('PDF loading error:', e);
                  setShowFallback(true);
                }}
                onLoad={(e) => {
                  console.log('PDF loaded successfully');
                  // Check if iframe loaded properly
                  try {
                    const iframe = e.target as HTMLIFrameElement;
                    if (iframe.contentWindow?.location.href === 'about:blank') {
                      setShowFallback(true);
                    }
                  } catch (error) {
                    // Cross-origin error is expected, means it's working
                  }
                }}
              />
            ) : (
              <div className="flex flex-col items-center justify-center h-full p-8 text-center">
                <div className="bg-white rounded-lg p-6 max-w-md">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    PDF Viewer Blocked
                  </h3>
                  <p className="text-gray-600 mb-6">
                    Your browser is blocking the PDF viewer. You can open the document in a new tab instead.
                  </p>
                  <div className="flex gap-3 justify-center">
                    <button
                      onClick={() => window.open(pdfUrl, '_blank')}
                      className="px-4 py-2 bg-rag-primary text-white rounded-lg hover:bg-rag-primary/90 transition-colors flex items-center gap-2"
                    >
                      <ArrowTopRightOnSquareIcon className="w-4 h-4" />
                      Open in New Tab
                    </button>
                    <button
                      onClick={() => setShowFallback(false)}
                      className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                    >
                      Try Again
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Footer */}
          <div className="p-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600">
                Click and drag to scroll • Use browser zoom controls to resize
              </p>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-rag-primary text-white rounded-lg hover:bg-rag-primary/90 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </Dialog.Panel>
      </div>
    </Dialog>
  );
};