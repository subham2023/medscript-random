from app.agents.orchestrator import OrchestratorAgent
from app.services import firestore_service
import datetime

async def analyze_document_in_background(document_id: str, extracted_text: str):
    """
    This function is the core of the background analysis task.
    It orchestrates the AI agents and updates Firestore with the results.
    """
    try:
        # 1. Update status to 'analyzing'
        await firestore_service.update_analysis_record(
            document_id,
            {"processing_status": "analyzing", "message": "AI analysis in progress."}
        )

        # 2. Initialize and run the orchestrator agent
        orchestrator_agent = OrchestratorAgent()
        orchestration_result = await orchestrator_agent.process_document(extracted_text)

        # 3. Prepare the final result document
        final_result = {
            "document_id": document_id,
            "document_type": orchestration_result.get("document_type", "unknown"),
            "summary": orchestration_result.get("summary", "No summary generated."),
            "key_findings": orchestration_result.get("key_findings", []),
            "extracted_entities": orchestration_result.get("extracted_entities", []),
            "safety_assessment": orchestration_result.get("safety_assessment", []),
            "processing_status": "complete",
            "message": "Analysis successful.",
            "completed_at": firestore_service.SERVER_TIMESTAMP,
        }

        # 4. Update the record in Firestore with the complete analysis
        await firestore_service.update_analysis_record(document_id, final_result)
        print(f"Successfully completed analysis for document_id: {document_id}")

    except Exception as e:
        print(f"Error during background analysis for document_id: {document_id}. Error: {e}")
        # Update Firestore with an error status
        await firestore_service.update_analysis_record(
            document_id,
            {
                "processing_status": "failed",
                "message": f"An unexpected error occurred: {str(e)}",
                "completed_at": firestore_service.SERVER_TIMESTAMP,
            }
        )