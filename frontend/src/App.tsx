import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatPage } from './pages/ChatPage';
import { apiService } from './services/api';
import { HealthStatus } from './types';

function App() {
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);

  useEffect(() => {
    checkHealth();
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const health = await apiService.getHealth();
      setHealthStatus(health);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealthStatus({
        status: 'unhealthy',
        services: {},
        timestamp: new Date().toISOString()
      });
    }
  };

  const handleSessionSelect = (sessionId: number) => {
    setCurrentSessionId(sessionId);
  };

  const handleNewSession = () => {
    setCurrentSessionId(null);
  };

  const handleSessionCreated = (sessionId: number) => {
    setCurrentSessionId(sessionId);
    // Refresh sidebar to show new session
    if ((window as any).refreshSidebar) {
      (window as any).refreshSidebar();
    }
  };

  const getHealthStatusColor = () => {
    if (!healthStatus) return 'bg-gray-500';
    switch (healthStatus.status) {
      case 'healthy': return 'bg-green-500';
      case 'degraded': return 'bg-yellow-500';
      case 'unhealthy': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getHealthStatusText = () => {
    if (!healthStatus) return 'Checking...';
    return healthStatus.status.charAt(0).toUpperCase() + healthStatus.status.slice(1);
  };

  return (
    <div className="h-screen bg-white flex">
      {/* Sidebar */}
      <Sidebar
        currentSessionId={currentSessionId}
        onSessionSelect={handleSessionSelect}
        onNewSession={handleNewSession}
      />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Health Status Bar */}
        <div className="bg-gray-50 border-b border-rag-border px-4 py-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm text-rag-secondary">
              <div className={`w-2 h-2 rounded-full ${getHealthStatusColor()}`} />
              <span>System Status: {getHealthStatusText()}</span>
              {healthStatus && (
                <span className="text-xs">
                  ({Object.entries(healthStatus.services).map(([service, status]) => 
                    `${service}: ${status}`
                  ).join(', ')})
                </span>
              )}
            </div>
            <div className="text-xs text-rag-secondary">
              🔒 Privacy-First RAG Chat
            </div>
          </div>
        </div>
        
        {/* Chat Page */}
        <ChatPage
          sessionId={currentSessionId}
          onSessionCreated={handleSessionCreated}
        />
      </div>
    </div>
  );
}

export default App;