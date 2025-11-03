import React, { useState, useCallback } from 'react';
import { useMedicalAnalysis } from '../hooks/useMedicalAnalysis';
import AnalysisDashboard from './AnalysisDashboard';

const DocumentUpload: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const { analysisResult, error, isLoading, statusMessage, uploadAndAnalyze } = useMedicalAnalysis();

    const handleFileChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setSelectedFile(event.target.files[0]);
        }
    }, []);

    const handleFileUpload = useCallback(async () => {
        if (selectedFile) {
            uploadAndAnalyze(selectedFile);
        }
    }, [selectedFile, uploadAndAnalyze]);

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
            <h1>Upload Medical Document for Analysis</h1>
            <p>Upload a PDF, JPG, PNG, or TXT file to get a clear, understandable summary of your medical information.</p>

            <div style={{ margin: '20px 0', border: '2px dashed #ccc', padding: '20px', borderRadius: '8px' }}>
                <input
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png,.txt"
                    onChange={handleFileChange}
                    disabled={isLoading}
                    style={{ display: 'block', marginBottom: '10px' }}
                />
                <button onClick={handleFileUpload} disabled={!selectedFile || isLoading}>
                    {isLoading ? 'Processing...' : 'Upload and Analyze'}
                </button>
            </div>

            {isLoading && (
                <div style={{ marginTop: '20px' }}>
                    <h3>Analysis in Progress...</h3>
                    <p>{statusMessage}</p>
                    {/* A simple spinner */}
                    <div className="spinner"></div>
                    <style>{`
                        .spinner {
                            border: 4px solid rgba(0, 0, 0, 0.1);
                            width: 36px;
                            height: 36px;
                            border-radius: 50%;
                            border-left-color: #09f;
                            animation: spin 1s ease infinite;
                            margin: 20px auto;
                        }
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    `}</style>
                </div>
            )}

            {error && <p style={{ color: 'red', marginTop: '20px' }}>Error: {error}</p>}

            {analysisResult && !isLoading && (
                <AnalysisDashboard result={analysisResult} />
            )}
        </div>
    );
};

export default DocumentUpload;