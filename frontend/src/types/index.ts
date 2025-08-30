export interface ChatSession {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface SourceReference {
  filename: string;
  page: number;
  content: string;
}

export interface ChatMessage {
  id: number;
  session_id: number;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceReference[];
  created_at: string;
}

export interface Document {
  filename: string;
  upload_date: string;
  pages: number;
  size_mb: number;
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  services: {
    [key: string]: 'healthy' | 'unhealthy';
  };
  timestamp: string;
}