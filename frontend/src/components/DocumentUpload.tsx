import React, { useState, useCallback } from 'react';
import { uploadDocument, AnalysisResult } from '../services/api';

const DocumentUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setAnalysisResult(null);
      setError(null);
    }
  }, []);

  const handleFileUpload = useCallback(async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const result = await uploadDocument(selectedFile);
      setAnalysisResult(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during upload.');
      console.error('Upload error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [selectedFile]);

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
      <h1>Upload Medical Document</h1>
      <input type="file" onChange={handleFileChange} disabled={isLoading} />
      <button onClick={handleFileUpload} disabled={!selectedFile || isLoading}>
        {isLoading ? 'Uploading...' : 'Upload and Analyze'}
      </button>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {analysisResult && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '15px' }}>
          <h2>Analysis Result</h2>
          <p><strong>Document ID:</strong> {analysisResult.document_id}</p>
          <p><strong>Document Type:</strong> {analysisResult.document_type}</p>
          <p><strong>Status:</strong> {analysisResult.processing_status}</p>
          <p><strong>Summary:</strong> {analysisResult.summary}</p>
          <h3>Key Findings:</h3>
          <ul>
            {analysisResult.key_findings.map((finding, index) => (
              <li key={index}>{finding}</li>
            ))}
          </ul>
          <h3>Extracted Entities:</h3>
          <ul>
            {analysisResult.extracted_entities.map((entity, index) => (
              <li key={index}>
                <strong>{entity.entity_type}:</strong> {entity.entity_value} (Confidence: {entity.confidence_score.toFixed(2)})
              </li>
            ))}
          </ul>
          <h3>Safety Assessment:</h3>
          <ul>
            {analysisResult.safety_assessment.map((alert, index) => (
              <li key={index} style={{ color: alert.severity === 'critical' ? 'red' : alert.severity === 'major' ? 'orange' : 'inherit' }}>
                <strong>{alert.title} ({alert.severity}):</strong> {alert.description}
                {alert.action_required && <em> (Action Required)</em>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
