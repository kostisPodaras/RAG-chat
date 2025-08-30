import { ChatSession, ChatMessage, Document, HealthStatus } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

class ApiService {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`API Error: ${response.status} - ${error}`);
    }

    return response.json();
  }

  // Health endpoints
  async getHealth(): Promise<HealthStatus> {
    return this.request<HealthStatus>('/api/v1/health');
  }

  // Chat endpoints
  async createChatSession(title: string): Promise<ChatSession> {
    return this.request<ChatSession>('/api/v1/chat/sessions', {
      method: 'POST',
      body: JSON.stringify({ title }),
    });
  }

  async getChatSessions(): Promise<ChatSession[]> {
    return this.request<ChatSession[]>('/api/v1/chat/sessions');
  }

  async getChatMessages(sessionId: number): Promise<ChatMessage[]> {
    return this.request<ChatMessage[]>(`/api/v1/chat/sessions/${sessionId}/messages`);
  }

  async sendMessage(sessionId: number, content: string): Promise<ChatMessage> {
    return this.request<ChatMessage>(`/api/v1/chat/sessions/${sessionId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ session_id: sessionId, content }),
    });
  }

  async deleteChatSession(sessionId: number): Promise<void> {
    await this.request(`/api/v1/chat/sessions/${sessionId}`, {
      method: 'DELETE',
    });
  }

  // Document endpoints
  async uploadDocument(file: File): Promise<{ filename: string; pages: number; message: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/v1/documents/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Upload failed: ${response.status} - ${error}`);
    }

    return response.json();
  }

  async getDocuments(): Promise<Document[]> {
    return this.request<Document[]>('/api/v1/documents');
  }

  async deleteDocument(filename: string): Promise<void> {
    await this.request(`/api/v1/documents/${encodeURIComponent(filename)}`, {
      method: 'DELETE',
    });
  }
}

export const apiService = new ApiService();