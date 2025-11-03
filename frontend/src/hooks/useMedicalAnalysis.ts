import { useState, useCallback } from 'react';
import { uploadDocument, getAnalysisStatus, getAnalysisResult, AnalysisResult, AnalysisStatus } from '../services/api';

const POLLING_INTERVAL = 3000; // 3 seconds

export const useMedicalAnalysis = () => {
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [statusMessage, setStatusMessage] = useState<string>('');

    const pollForResults = useCallback(async (documentId: string) => {
        try {
            const statusResponse = await getAnalysisStatus(documentId);

            if (statusResponse.status === 'complete') {
                const finalResult = await getAnalysisResult(documentId);
                setAnalysisResult(finalResult);
                setStatusMessage('Analysis complete!');
                setIsLoading(false);
            } else if (statusResponse.status === 'failed') {
                setError(statusResponse.message || 'Analysis failed.');
                setIsLoading(false);
            } else {
                // Status is 'processing' or another intermediate state
                setStatusMessage(statusResponse.message || 'Analysis is in progress...');
                setTimeout(() => pollForResults(documentId), POLLING_INTERVAL);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'An error occurred while polling for results.');
            setIsLoading(false);
        }
    }, []);

    const uploadAndAnalyze = useCallback(async (file: File) => {
        setIsLoading(true);
        setError(null);
        setAnalysisResult(null);
        setStatusMessage('Uploading document...');

        try {
            // This now returns an AnalysisStatus immediately
            const initialResponse = await uploadDocument(file);
            setStatusMessage('Document uploaded. Starting analysis...');

            // Start polling for the final result
            if (initialResponse.document_id) {
                pollForResults(initialResponse.document_id);
            } else {
                throw new Error("Did not receive a document ID from the server.");
            }

        } catch (err: any) {
            setError(err.response?.data?.detail || 'An error occurred during upload.');
            setIsLoading(false);
        }
    }, [pollForResults]);

    return { analysisResult, error, isLoading, statusMessage, uploadAndAnalyze };
};