import axios from 'axios';

// Use production backend URL as default, fallback to localhost only in development
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://medscript-ai-backend-1074963275925.us-central1.run.app/api/v1'
    : 'http://localhost:8000/api/v1');

interface MedicalEntity {
  entity_type: string;
  entity_value: string;
  confidence_score: number;
  metadata?: Record<string, any>;
}

interface SafetyAlert {
  severity: string;
  title: string;
  description: string;
  action_required: boolean;
}

export interface AnalysisResult {
  document_id: string;
  document_type: string;
  summary: string;
  key_findings: string[];
  extracted_entities: MedicalEntity[];
  safety_assessment: SafetyAlert[];
  processing_status: string;
}

export interface UploadResponse {
  document_id: string;
  file_name: string;
  gcs_path: string;
  status: string;
  message: string;
}

export interface AnalysisStatus {
  document_id: string;
  status: string;
  message?: string;
}

export const uploadDocument = async (file: File): Promise<AnalysisStatus> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post<AnalysisStatus>(`${API_BASE_URL}/documents/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getAnalysisStatus = async (documentId: string): Promise<AnalysisStatus> => {
  const response = await axios.get<AnalysisStatus>(`${API_BASE_URL}/analysis/${documentId}/status`);
  return response.data;
};

export const getAnalysisResult = async (documentId: string): Promise<AnalysisResult> => {
  const response = await axios.get<AnalysisResult>(`${API_BASE_URL}/analysis/${documentId}`);
  return response.data;
};
