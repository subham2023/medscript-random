import axios from 'axios';

// Use environment variable for the API base URL
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface MedicalEntity {
  entity_type: string;
  entity_value: string;
  confidence_score: number;
  metadata?: Record<string, any>;
}

export interface SafetyAlert {
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

export interface AnalysisStatus {
  document_id: string;
  status: string;
  message?: string;
}

/**
 * Uploads a document and starts the analysis.
 * Returns the initial status of the analysis task.
 */
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

/**
 * Gets the current status of an analysis task.
 */
export const getAnalysisStatus = async (documentId: string): Promise<AnalysisStatus> => {
  const response = await axios.get<AnalysisStatus>(`${API_BASE_URL}/analysis/${documentId}/status`);
  return response.data;
};

/**
 * Gets the final result of a completed analysis.
 */
export const getAnalysisResult = async (documentId: string): Promise<AnalysisResult> => {
  const response = await axios.get<AnalysisResult>(`${API_BASE_URL}/analysis/${documentId}`);
  return response.data;
};